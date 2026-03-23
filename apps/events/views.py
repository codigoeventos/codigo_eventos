"""
Event views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError

from apps.common.mixins import AuditMixin
from .models import Event
from .forms import EventForm, EventSearchForm
from apps.contractors.models import Contractor, ContractorMember, EventContractor, EventContractorMember


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
            'contractors__selected_members__member',
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


# ─── Contractor Assignment Views ──────────────────────────────────────────────

class ContractorMembersJSONView(LoginRequiredMixin, View):
    """Return JSON list of members for a given contractor (for dynamic loading)."""

    def get(self, request):
        contractor_id = request.GET.get('contractor_id')
        if not contractor_id:
            return JsonResponse({'members': []})
        members = ContractorMember.objects.filter(
            contractor_id=contractor_id
        ).order_by('name').values('id', 'name', 'role')
        return JsonResponse({'members': list(members)})


class ContractorAssignView(LoginRequiredMixin, View):
    """Assign a (new) contractor to an event and select participating members."""

    template_name = 'events/event_assign_contractor.html'

    def _get_event(self, pk):
        return get_object_or_404(Event, pk=pk)

    def get(self, request, pk):
        event = self._get_event(pk)
        assigned_ids = event.contractors.values_list('contractor_id', flat=True)
        contractors = Contractor.objects.exclude(pk__in=assigned_ids).order_by('name')
        return render(request, self.template_name, {
            'event': event,
            'contractors': contractors,
            'assignment': None,
            'selected_member_ids': [],
            'breadcrumbs': [
                {'name': 'Eventos', 'url': reverse('events:list')},
                {'name': event.name, 'url': reverse('events:detail', kwargs={'pk': pk})},
                {'name': 'Vincular Empreiteira', 'url': None},
            ],
        })

    def post(self, request, pk):
        event = self._get_event(pk)
        contractor_id = request.POST.get('contractor')
        member_ids = request.POST.getlist('members')
        notes = request.POST.get('notes', '')
        error = None

        if not contractor_id:
            error = 'Selecione uma empreiteira.'
        else:
            try:
                assignment, _ = EventContractor.objects.get_or_create(
                    event=event,
                    contractor_id=contractor_id,
                    defaults={'notes': notes},
                )
                assignment.notes = notes
                assignment.save(update_fields=['notes'])
                assignment.selected_members.all().delete()
                for mid in member_ids:
                    EventContractorMember.objects.create(assignment=assignment, member_id=mid)
                return redirect('events:detail', pk=pk)
            except ValidationError as e:
                error = ' '.join(e.messages)

        assigned_ids = event.contractors.values_list('contractor_id', flat=True)
        contractors = Contractor.objects.exclude(pk__in=assigned_ids).order_by('name')
        return render(request, self.template_name, {
            'event': event,
            'contractors': contractors,
            'assignment': None,
            'selected_member_ids': member_ids,
            'error': error,
            'breadcrumbs': [
                {'name': 'Eventos', 'url': reverse('events:list')},
                {'name': event.name, 'url': reverse('events:detail', kwargs={'pk': pk})},
                {'name': 'Vincular Empreiteira', 'url': None},
            ],
        })


class ContractorAssignEditView(LoginRequiredMixin, View):
    """Edit the member selection for an existing contractor assignment."""

    template_name = 'events/event_assign_contractor.html'

    def _get_objects(self, pk, assignment_pk):
        event = get_object_or_404(Event, pk=pk)
        assignment = get_object_or_404(EventContractor, pk=assignment_pk, event=event)
        return event, assignment

    def get(self, request, pk, assignment_pk):
        event, assignment = self._get_objects(pk, assignment_pk)
        selected_ids = list(assignment.selected_members.values_list('member_id', flat=True))
        return render(request, self.template_name, {
            'event': event,
            'contractors': [assignment.contractor],
            'assignment': assignment,
            'selected_member_ids': selected_ids,
            'breadcrumbs': [
                {'name': 'Eventos', 'url': reverse('events:list')},
                {'name': event.name, 'url': reverse('events:detail', kwargs={'pk': pk})},
                {'name': 'Editar Membros', 'url': None},
            ],
        })

    def post(self, request, pk, assignment_pk):
        event, assignment = self._get_objects(pk, assignment_pk)
        member_ids = request.POST.getlist('members')
        notes = request.POST.get('notes', '')
        assignment.notes = notes
        assignment.save(update_fields=['notes'])
        assignment.selected_members.all().delete()
        for mid in member_ids:
            EventContractorMember.objects.create(assignment=assignment, member_id=mid)
        return redirect('events:detail', pk=pk)


class ContractorAssignRemoveView(LoginRequiredMixin, View):
    """Remove a contractor (and its members) from an event."""

    def post(self, request, pk, assignment_pk):
        assignment = get_object_or_404(EventContractor, pk=assignment_pk, event_id=pk)
        assignment.delete()
        return redirect('events:detail', pk=pk)
