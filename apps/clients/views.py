"""
Client views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import PermissionRequiredMixin, AuditMixin
from .models import Client
from .forms import ClientForm, ClientSearchForm


class ClientListView(LoginRequiredMixin, ListView):
    """List all clients with search and pagination."""
    
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    # permission_required = 'clients.view_client'  # Commented out for now
    paginate_by = 20
    
    def get_queryset(self):
        """Filter clients based on search query."""
        queryset = Client.objects.select_related('created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(document_number__icontains=search)
            )
        
        # Filter by document type
        document_type = self.request.GET.get('document_type', '').strip()
        if document_type:
            queryset = queryset.filter(document_type=document_type)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = ClientSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': None}
        ]
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Display client details and related events."""
    
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'
   # permission_required = 'clients.view_client'  # Commented out for now
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Client.objects.select_related(
            'created_by',
            'updated_by'
        ).prefetch_related('events')
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse_lazy('clients:list')},
            {'name': self.object.name, 'url': None}
        ]
        # Get related events
        context['events'] = self.object.events.all().order_by('-event_date')[:5]
        return context


class ClientCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new client."""
    
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    # permission_required = 'clients.add_client'  # Commented out for now
    success_message = "Cliente %(name)s criado com sucesso!"
    
    def get_success_url(self):
        """Redirect to client detail after creation."""
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse_lazy('clients:list')},
            {'name': 'Novo Cliente', 'url': None}
        ]
        context['form_title'] = 'Novo Cliente'
        context['submit_text'] = 'Criar Cliente'
        return context


class ClientUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing client."""
    
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    # permission_required = 'clients.change_client'  # Commented out for now
    success_message = "Cliente %(name)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to client detail after update."""
        return reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse_lazy('clients:list')},
            {'name': self.object.name, 'url': reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Cliente: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context


class ClientDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete a client (soft delete)."""
    
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    # permission_required = 'clients.delete_client'  # Commented out for now
    success_url = reverse_lazy('clients:list')
    success_message = "Cliente excluído com sucesso!"
    
    def delete(self, request, *args, **kwargs):
        """Handle delete request - supports both AJAX and regular POST."""
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # Perform soft delete
        self.object.delete()
        
        # If AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'message': self.success_message
            })
        
        # Regular request - redirect with message
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Clientes', 'url': reverse_lazy('clients:list')},
            {'name': self.object.name, 'url': reverse_lazy('clients:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Excluir', 'url': None}
        ]
        return context
