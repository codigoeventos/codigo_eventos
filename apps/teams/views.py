"""
Team views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction

from apps.common.mixins import AuditMixin
from .models import Team, TeamMember
from .forms import TeamForm, TeamSearchForm, TeamMemberFormSet


class TeamMemberListView(LoginRequiredMixin, ListView):
    """List all teams with search and pagination."""
    
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter teams based on search query."""
        queryset = Team.objects.prefetch_related('members').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = TeamSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': None}
        ]
        return context


class TeamMemberDetailView(LoginRequiredMixin, DetailView):
    """Display team details and members."""
    
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Team.objects.prefetch_related('members', 'created_by', 'updated_by')
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class TeamMemberCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new team with members."""
    
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_message = "Equipe %(name)s criada com sucesso!"
    
    def get_success_url(self):
        """Redirect to team detail after creation."""
        return reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['members_formset'] = TeamMemberFormSet(self.request.POST, instance=self.object)
        else:
            context['members_formset'] = TeamMemberFormSet(instance=self.object)
        
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': 'Nova Equipe', 'url': None}
        ]
        context['form_title'] = 'Nova Equipe'
        context['submit_text'] = 'Criar Equipe'
        return context
    
    def form_valid(self, form):
        """Save team and members."""
        context = self.get_context_data()
        members_formset = context['members_formset']
        
        # Set audit fields
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            if members_formset.is_valid():
                members_formset.instance = self.object
                members_formset.save()
            else:
                return self.form_invalid(form)
        
        return super(TeamMemberCreateView, self).form_valid(form)


class TeamMemberUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing team and its members."""
    
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_message = "Equipe %(name)s atualizada com sucesso!"
    
    def get_success_url(self):
        """Redirect to team detail after update."""
        return reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['members_formset'] = TeamMemberFormSet(self.request.POST, instance=self.object)
        else:
            context['members_formset'] = TeamMemberFormSet(instance=self.object)
        
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': self.object.name, 'url': reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Equipe: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        """Save team and members."""
        context = self.get_context_data()
        members_formset = context['members_formset']
        
        # Set audit field
        form.instance.updated_by = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            if members_formset.is_valid():
                members_formset.instance = self.object
                members_formset.save()
            else:
                return self.form_invalid(form)
        
        return super(TeamMemberUpdateView, self).form_valid(form)


class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a team - via AJAX only."""
    
    model = Team
    success_url = reverse_lazy('teams:list')
    success_message = "Equipe excluída com sucesso!"
    
    def post(self, request, *args, **kwargs):
        """Handle POST delete request - AJAX only."""
        self.object = self.get_object()
        
        # Soft delete (BaseModel handles this)
        self.object.delete()
        
        return JsonResponse({
            'success': True,
            'message': self.success_message
        })
    
    def get(self, request, *args, **kwargs):
        """Redirect GET requests to team detail page."""
        team = self.get_object()
        return HttpResponseRedirect(reverse_lazy('teams:detail', kwargs={'pk': team.pk}))
