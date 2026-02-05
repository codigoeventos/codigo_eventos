"""
Technical Visit views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import AuditMixin
from .models import TechnicalVisit
from .forms import TechnicalVisitForm, TechnicalVisitSearchForm


class TechnicalVisitListView(LoginRequiredMixin, ListView):
    """List all technical visits with search and pagination."""
    
    model = TechnicalVisit
    template_name = 'technical_visits/technicalvisit_list.html'
    context_object_name = 'technical_visits'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter technical visits based on search query."""
        queryset = TechnicalVisit.objects.select_related('event', 'event__client', 'responsible', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(event__name__icontains=search) |
                Q(event__client__name__icontains=search) |
                Q(responsible__name__icontains=search) |
                Q(notes__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by event
        event = self.request.GET.get('event', '').strip()
        if event:
            queryset = queryset.filter(event_id=event)
        
        return queryset.order_by('-visit_date')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = TechnicalVisitSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Visitas Técnicas', 'url': None}
        ]
        return context


class TechnicalVisitDetailView(LoginRequiredMixin, DetailView):
    """Display technical visit details and related data."""
    
    model = TechnicalVisit
    template_name = 'technical_visits/technicalvisit_detail.html'
    context_object_name = 'technical_visit'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return TechnicalVisit.objects.select_related(
            'event',
            'event__client',
            'responsible',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'attachments'
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Visitas Técnicas', 'url': reverse_lazy('technical_visits:list')},
            {'name': f'Visita - {self.object.event.name}', 'url': None}
        ]
        return context


class TechnicalVisitCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new technical visit."""
    
    model = TechnicalVisit
    form_class = TechnicalVisitForm
    template_name = 'technical_visits/technicalvisit_form.html'
    success_message = "Visita Técnica criada com sucesso!"
    
    def get_success_url(self):
        """Redirect to technical visit detail after creation."""
        return reverse_lazy('technical_visits:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Visitas Técnicas', 'url': reverse_lazy('technical_visits:list')},
            {'name': 'Nova Visita Técnica', 'url': None}
        ]
        context['form_title'] = 'Nova Visita Técnica'
        context['submit_text'] = 'Criar Visita Técnica'
        return context


class TechnicalVisitUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing technical visit."""
    
    model = TechnicalVisit
    form_class = TechnicalVisitForm
    template_name = 'technical_visits/technicalvisit_form.html'
    success_message = "Visita Técnica atualizada com sucesso!"
    
    def get_success_url(self):
        """Redirect to technical visit detail after update."""
        return reverse_lazy('technical_visits:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Visitas Técnicas', 'url': reverse_lazy('technical_visits:list')},
            {'name': f'Visita - {self.object.event.name}', 'url': reverse_lazy('technical_visits:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Visita Técnica: {self.object.event.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class TechnicalVisitDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a technical visit (soft delete) - via AJAX only."""
    
    model = TechnicalVisit
    success_url = reverse_lazy('technical_visits:list')
    success_message = "Visita Técnica excluída com sucesso!"
    
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
        """Redirect GET requests to technical visit detail page."""
        technical_visit = self.get_object()
        return HttpResponseRedirect(reverse_lazy('technical_visits:detail', kwargs={'pk': technical_visit.pk}))
