"""
Team views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from .models import TeamMember
from .forms import TeamMemberForm, TeamMemberSearchForm


class TeamMemberListView(LoginRequiredMixin, ListView):
    """List all team members with search and pagination."""
    
    model = TeamMember
    template_name = 'teams/team_member_list.html'
    context_object_name = 'members'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter team members based on search query."""
        queryset = TeamMember.objects.all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(role__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = TeamMemberSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': None}
        ]
        return context


class TeamMemberDetailView(LoginRequiredMixin, DetailView):
    """Display team member details."""
    
    model = TeamMember
    template_name = 'teams/team_member_detail.html'
    context_object_name = 'member'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return TeamMember.objects.prefetch_related('event_assignments__event')
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class TeamMemberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create a new team member."""
    
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'teams/team_member_form.html'
    success_message = "Membro %(name)s adicionado com sucesso!"
    
    def get_success_url(self):
        """Redirect to team member detail after creation."""
        return reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': 'Novo Membro', 'url': None}
        ]
        context['form_title'] = 'Novo Membro da Equipe'
        context['submit_text'] = 'Adicionar Membro'
        return context


class TeamMemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update an existing team member."""
    
    model = TeamMember
    form_class = TeamMemberForm
    template_name = 'teams/team_member_form.html'
    success_message = "Membro %(name)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to team member detail after update."""
        return reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Equipes', 'url': reverse_lazy('teams:list')},
            {'name': self.object.name, 'url': reverse_lazy('teams:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Membro: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class TeamMemberDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a team member - via AJAX only."""
    
    model = TeamMember
    success_url = reverse_lazy('teams:list')
    success_message = "Membro excluído com sucesso!"
    
    def post(self, request, *args, **kwargs):
        """Handle POST delete request - AJAX only."""
        self.object = self.get_object()
        self.object.delete()
        
        return JsonResponse({
            'success': True,
            'message': self.success_message
        })
    
    def get(self, request, *args, **kwargs):
        """Redirect GET requests to member detail page."""
        member = self.get_object()
        return HttpResponseRedirect(reverse_lazy('teams:detail', kwargs={'pk': member.pk}))
