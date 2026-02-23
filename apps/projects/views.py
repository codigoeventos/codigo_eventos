"""
Project views for Event Management System.
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import AuditMixin
from .models import Project, ProjectFile
from .forms import ProjectForm, ProjectSearchForm, ProjectFileForm


class ProjectListView(LoginRequiredMixin, ListView):
    """List all projects with search and pagination."""
    
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter projects based on search query."""
        queryset = Project.objects.select_related('event', 'event__client', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(event__name__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by event
        event = self.request.GET.get('event', '').strip()
        if event:
            queryset = queryset.filter(event_id=event)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProjectSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': None}
        ]
        return context


class ProjectDetailView(LoginRequiredMixin, DetailView):
    """Display project details and related data."""
    
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Project.objects.select_related(
            'event',
            'event__client',
            'contractor',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'budgets',
            'budgets__items',
            'files',
            'files__uploaded_by',
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': reverse_lazy('projects:list')},
            {'name': self.object.title, 'url': None}
        ]
        return context


class ProjectCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new project."""
    
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_message = "Projeto %(title)s criado com sucesso!"
    
    def get_success_url(self):
        """Redirect to project detail after creation."""
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
    
    def get_initial(self):
        """Pre-fill event if event_id is passed as query param."""
        initial = super().get_initial()
        event_id = self.request.GET.get('event')
        if event_id:
            initial['event'] = event_id
        return initial

    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': reverse_lazy('projects:list')},
            {'name': 'Novo Projeto', 'url': None}
        ]
        context['form_title'] = 'Novo Projeto'
        context['submit_text'] = 'Criar Projeto'
        return context


class ProjectUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing project."""
    
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_message = "Projeto %(title)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to project detail after update."""
        return reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': reverse_lazy('projects:list')},
            {'name': self.object.title, 'url': reverse_lazy('projects:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Projeto: {self.object.title}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a project (soft delete) - via AJAX only."""
    
    model = Project
    success_url = reverse_lazy('projects:list')
    success_message = "Projeto excluído com sucesso!"
    
    def post(self, request, *args, **kwargs):
        """Handle POST delete request - AJAX only."""
        self.object = self.get_object()
        
        # Perform soft delete
        self.object.delete()
        
        # Return JSON response
        return JsonResponse({
            'success': True,
            'message': self.success_message
        })
    
    def get(self, request, *args, **kwargs):
        """Redirect GET requests to project detail page."""
        project = self.get_object()
        return HttpResponseRedirect(reverse_lazy('projects:detail', kwargs={'pk': project.pk}))


class ProjectFileCreateView(LoginRequiredMixin, View):
    """Upload a new file to a project."""

    def post(self, request, project_pk):
        project = get_object_or_404(Project, pk=project_pk)
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project_file = form.save(commit=False)
            project_file.project = project
            project_file.uploaded_by = request.user
            project_file.save()
            messages.success(request, f'Arquivo "{project_file.name}" enviado com sucesso!')
        else:
            messages.error(request, 'Erro ao enviar arquivo. Verifique os campos.')
        return redirect('projects:detail', pk=project_pk)

    def get(self, request, project_pk):
        return redirect('projects:detail', pk=project_pk)


class ProjectFileDeleteView(LoginRequiredMixin, View):
    """Delete a project file – POST only."""

    def post(self, request, pk):
        project_file = get_object_or_404(ProjectFile, pk=pk)
        project_pk = project_file.project_id
        name = project_file.name
        project_file.file.delete(save=False)
        project_file.delete()
        messages.success(request, f'Arquivo "{name}" excluído.')
        return redirect('projects:detail', pk=project_pk)

    def get(self, request, pk):
        project_file = get_object_or_404(ProjectFile, pk=pk)
        return redirect('projects:detail', pk=project_file.project_id)

