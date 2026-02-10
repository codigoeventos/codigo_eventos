"""
Budget views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

from apps.common.mixins import AuditMixin
from .models import Budget
from .forms import BudgetForm, BudgetSearchForm, BudgetItemFormSet


class BudgetListView(LoginRequiredMixin, ListView):
    """List all budgets with search and pagination."""
    
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter budgets based on search query."""
        queryset = Budget.objects.select_related('proposal', 'proposal__event', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(proposal__title__icontains=search) |
                Q(proposal__event__name__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by proposal
        proposal = self.request.GET.get('proposal', '').strip()
        if proposal:
            queryset = queryset.filter(proposal_id=proposal)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = BudgetSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': None}
        ]
        return context


class BudgetDetailView(LoginRequiredMixin, DetailView):
    """Display budget details and related data."""
    
    model = Budget
    template_name = 'budgets/budget_detail.html'
    context_object_name = 'budget'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Budget.objects.select_related(
            'proposal',
            'proposal__event',
            'proposal__event__client',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'items'
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class BudgetCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new budget."""
    
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_message = "Orçamento %(name)s criado com sucesso!"
    
    def get_success_url(self):
        """Redirect to budget detail after creation."""
        return reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': 'Novo Orçamento', 'url': None}
        ]
        context['form_title'] = 'Novo Orçamento'
        context['submit_text'] = 'Criar Orçamento'
        
        if self.request.POST:
            context['items_formset'] = BudgetItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = BudgetItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        """Save budget and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class BudgetUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing budget."""
    
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_message = "Orçamento %(name)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to budget detail after update."""
        return reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': self.object.name, 'url': reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Orçamento: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        
        if self.request.POST:
            context['items_formset'] = BudgetItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = BudgetItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        """Save budget and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a budget (soft delete) - via AJAX only."""
    
    model = Budget
    success_url = reverse_lazy('budgets:list')
    success_message = "Orçamento excluído com sucesso!"
    
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
        """Redirect GET requests to budget detail page."""
        budget = self.get_object()
        return HttpResponseRedirect(reverse_lazy('budgets:detail', kwargs={'pk': budget.pk}))
