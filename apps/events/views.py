"""
Event views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import AuditMixin
from .models import Event
from .forms import EventForm, EventSearchForm


class EventListView(LoginRequiredMixin, ListView):
    """List all events with search and pagination."""
    
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter events based on search query."""
        queryset = Event.objects.select_related('client', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(client__name__icontains=search)
            )
        
        # Filter by client
        client = self.request.GET.get('client', '').strip()
        if client:
            queryset = queryset.filter(client_id=client)
        
        return queryset.order_by('-event_date')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = EventSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Eventos', 'url': None}
        ]
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    """Display event details and related data."""
    
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Event.objects.select_related(
            'client',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'projects',
            'service_orders',
            'technical_visits',
            'contractors__contractor',
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Eventos', 'url': reverse_lazy('events:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class EventCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new event."""
    
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_message = "Evento %(name)s criado com sucesso!"
    
    def get_success_url(self):
        """Redirect to event detail after creation."""
        return reverse_lazy('events:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Eventos', 'url': reverse_lazy('events:list')},
            {'name': 'Novo Evento', 'url': None}
        ]
        context['form_title'] = 'Novo Evento'
        context['submit_text'] = 'Criar Evento'
        return context


class EventUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing event."""
    
    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_message = "Evento %(name)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to event detail after update."""
        return reverse_lazy('events:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Eventos', 'url': reverse_lazy('events:list')},
            {'name': self.object.name, 'url': reverse_lazy('events:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Evento: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class EventDeleteView(LoginRequiredMixin, DeleteView):
    """Delete an event (soft delete) - via AJAX only."""
    
    model = Event
    success_url = reverse_lazy('events:list')
    success_message = "Evento excluído com sucesso!"
    
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
        """Redirect GET requests to event detail page."""
        event = self.get_object()
        return HttpResponseRedirect(reverse_lazy('events:detail', kwargs={'pk': event.pk}))
