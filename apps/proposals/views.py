"""
Proposal views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import AuditMixin
from .models import Proposal
from .forms import ProposalForm, ProposalSearchForm


class ProposalListView(LoginRequiredMixin, ListView):
    """List all proposals with search and pagination."""
    
    model = Proposal
    template_name = 'proposals/proposal_list.html'
    context_object_name = 'proposals'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter proposals based on search query."""
        queryset = Proposal.objects.select_related('event', 'event__client', 'created_by', 'updated_by').all()
        
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
        context['search_form'] = ProposalSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Propostas', 'url': None}
        ]
        return context


class ProposalDetailView(LoginRequiredMixin, DetailView):
    """Display proposal details and related data."""
    
    model = Proposal
    template_name = 'proposals/proposal_detail.html'
    context_object_name = 'proposal'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Proposal.objects.select_related(
            'event',
            'event__client',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'budgets',
            'budgets__items'
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Propostas', 'url': reverse_lazy('proposals:list')},
            {'name': self.object.title, 'url': None}
        ]
        return context


class ProposalCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new proposal."""
    
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_message = "Proposta %(title)s criada com sucesso!"
    
    def get_success_url(self):
        """Redirect to proposal detail after creation."""
        return reverse_lazy('proposals:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Propostas', 'url': reverse_lazy('proposals:list')},
            {'name': 'Nova Proposta', 'url': None}
        ]
        context['form_title'] = 'Nova Proposta'
        context['submit_text'] = 'Criar Proposta'
        return context


class ProposalUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing proposal."""
    
    model = Proposal
    form_class = ProposalForm
    template_name = 'proposals/proposal_form.html'
    success_message = "Proposta %(title)s atualizada com sucesso!"
    
    def get_success_url(self):
        """Redirect to proposal detail after update."""
        return reverse_lazy('proposals:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Propostas', 'url': reverse_lazy('proposals:list')},
            {'name': self.object.title, 'url': reverse_lazy('proposals:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Proposta: {self.object.title}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a proposal (soft delete) - via AJAX only."""
    
    model = Proposal
    success_url = reverse_lazy('proposals:list')
    success_message = "Proposta excluída com sucesso!"
    
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
        """Redirect GET requests to proposal detail page."""
        proposal = self.get_object()
        return HttpResponseRedirect(reverse_lazy('proposals:detail', kwargs={'pk': proposal.pk}))
