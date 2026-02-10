"""
Service Order views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.db import transaction

from apps.common.mixins import AuditMixin
from .models import ServiceOrder
from .forms import ServiceOrderForm, ServiceOrderSearchForm, ServiceOrderItemFormSet


class ServiceOrderListView(LoginRequiredMixin, ListView):
    """List all service orders with search and pagination."""
    
    model = ServiceOrder
    template_name = 'service_orders/serviceorder_list.html'
    context_object_name = 'service_orders'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter service orders based on search query."""
        queryset = ServiceOrder.objects.select_related('budget', 'event', 'event__client', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(event__name__icontains=search) |
                Q(event__client__name__icontains=search) |
                Q(budget__name__icontains=search)
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
        context['search_form'] = ServiceOrderSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': None}
        ]
        return context


class ServiceOrderDetailView(LoginRequiredMixin, DetailView):
    """Display service order details and related data."""
    
    model = ServiceOrder
    template_name = 'service_orders/serviceorder_detail.html'
    context_object_name = 'service_order'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return ServiceOrder.objects.select_related(
            'budget',
            'budget__proposal',
            'event',
            'event__client',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'items'
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': reverse_lazy('service_orders:list')},
            {'name': f'OS #{self.object.pk}', 'url': None}
        ]
        return context


class ServiceOrderCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new service order."""
    
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = 'service_orders/serviceorder_form.html'
    success_message = "Ordem de Serviço criada com sucesso!"
    
    def get_success_url(self):
        """Redirect to service order detail after creation."""
        return reverse_lazy('service_orders:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = ServiceOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = ServiceOrderItemFormSet(instance=self.object)
        
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': reverse_lazy('service_orders:list')},
            {'name': 'Nova Ordem de Serviço', 'url': None}
        ]
        context['form_title'] = 'Nova Ordem de Serviço'
        context['submit_text'] = 'Criar Ordem de Serviço'
        return context
    
    def form_valid(self, form):
        """Save service order and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        # Set audit fields (created_by)
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            if items_formset.is_valid():
                items_formset.instance = self.object
                items_formset.save()
            else:
                return self.form_invalid(form)
        
        return super(ServiceOrderCreateView, self).form_valid(form)


class ServiceOrderUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing service order."""
    
    model = ServiceOrder
    form_class = ServiceOrderForm
    template_name = 'service_orders/serviceorder_form.html'
    success_message = "Ordem de Serviço atualizada com sucesso!"
    
    def get_success_url(self):
        """Redirect to service order detail after update."""
        return reverse_lazy('service_orders:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = ServiceOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = ServiceOrderItemFormSet(instance=self.object)
        
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': reverse_lazy('service_orders:list')},
            {'name': f'OS #{self.object.pk}', 'url': reverse_lazy('service_orders:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Ordem de Serviço: OS #{self.object.pk}'
        context['submit_text'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        """Save service order and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        # Set audit field (updated_by)
        form.instance.updated_by = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            if items_formset.is_valid():
                items_formset.instance = self.object
                items_formset.save()
            else:
                return self.form_invalid(form)
        
        return super(ServiceOrderUpdateView, self).form_valid(form)


class ServiceOrderDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a service order (hard delete) - via AJAX only."""
    
    model = ServiceOrder
    success_url = reverse_lazy('service_orders:list')
    success_message = "Ordem de Serviço excluída com sucesso!"
    
    def post(self, request, *args, **kwargs):
        """Handle POST delete request - AJAX only."""
        self.object = self.get_object()
        
        # Perform HARD delete to allow recreating OS with same budget
        # Use Django's Model.delete() directly to bypass safedelete
        super(ServiceOrder, self.object).delete()
        
        # Return JSON response
        return JsonResponse({
            'success': True,
            'message': self.success_message
        })
    
    def get(self, request, *args, **kwargs):
        """Redirect GET requests to service order detail page."""
        service_order = self.get_object()
        return HttpResponseRedirect(reverse_lazy('service_orders:detail', kwargs={'pk': service_order.pk}))
