"""
Contractor views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404

from apps.common.mixins import AuditMixin
from .models import Contractor, ContractorMember
from .forms import ContractorForm, ContractorSearchForm, ContractorMemberForm


class ContractorListView(LoginRequiredMixin, ListView):
    """List all contractors with search and pagination."""

    model = Contractor
    template_name = 'contractors/contractor_list.html'
    context_object_name = 'contractors'
    paginate_by = 20

    def get_queryset(self):
        queryset = Contractor.objects.prefetch_related('members').all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(trade_name__icontains=search) |
                Q(cnpj__icontains=search) |
                Q(legal_representative__icontains=search)
            )
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ContractorSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': None}
        ]
        return context


class ContractorDetailView(LoginRequiredMixin, DetailView):
    """Display contractor details and members."""

    model = Contractor
    template_name = 'contractors/contractor_detail.html'
    context_object_name = 'contractor'

    def get_queryset(self):
        return Contractor.objects.prefetch_related('members')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class ContractorCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new contractor."""

    model = Contractor
    form_class = ContractorForm
    template_name = 'contractors/contractor_form.html'
    success_message = "Empreiteira %(name)s criada com sucesso!"

    def get_success_url(self):
        return reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': 'Nova Empreiteira', 'url': None}
        ]
        context['form_title'] = 'Nova Empreiteira'
        context['submit_text'] = 'Criar Empreiteira'
        return context

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ContractorUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing contractor."""

    model = Contractor
    form_class = ContractorForm
    template_name = 'contractors/contractor_form.html'
    success_message = "Empreiteira %(name)s atualizada com sucesso!"

    def get_success_url(self):
        return reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': self.object.name, 'url': reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Empreiteira: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ContractorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a contractor – via AJAX only."""

    model = Contractor
    success_url = reverse_lazy('contractors:list')
    success_message = "Empreiteira excluída com sucesso!"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True, 'message': self.success_message})

    def get(self, request, *args, **kwargs):
        contractor = self.get_object()
        return HttpResponseRedirect(reverse_lazy('contractors:detail', kwargs={'pk': contractor.pk}))


# ---------------------------------------------------------------------------
# ContractorMember CRUD
# ---------------------------------------------------------------------------

class MemberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Add a member to a contractor."""

    model = ContractorMember
    form_class = ContractorMemberForm
    template_name = 'contractors/member_form.html'
    success_message = "Membro %(name)s adicionado com sucesso!"

    def get_contractor(self):
        return get_object_or_404(Contractor, pk=self.kwargs['contractor_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contractor = self.get_contractor()
        context['contractor'] = contractor
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': contractor.name, 'url': reverse_lazy('contractors:detail', kwargs={'pk': contractor.pk})},
            {'name': 'Novo Membro', 'url': None},
        ]
        context['form_title'] = f'Novo Membro – {contractor.name}'
        context['submit_text'] = 'Adicionar Membro'
        return context

    def form_valid(self, form):
        form.instance.contractor = self.get_contractor()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contractors:detail', kwargs={'pk': self.kwargs['contractor_pk']})


class MemberDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a contractor member."""

    model = ContractorMember
    template_name = 'contractors/member_detail.html'
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contractor = self.object.contractor
        context['contractor'] = contractor
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': contractor.name, 'url': reverse_lazy('contractors:detail', kwargs={'pk': contractor.pk})},
            {'name': self.object.name, 'url': None},
        ]
        return context


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Update a contractor member."""

    model = ContractorMember
    form_class = ContractorMemberForm
    template_name = 'contractors/member_form.html'
    success_message = "Membro %(name)s atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contractor = self.object.contractor
        context['contractor'] = contractor
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': contractor.name, 'url': reverse_lazy('contractors:detail', kwargs={'pk': contractor.pk})},
            {'name': self.object.name, 'url': reverse_lazy('contractors:member_detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None},
        ]
        context['form_title'] = f'Editar Membro: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context

    def get_success_url(self):
        return reverse_lazy('contractors:member_detail', kwargs={'pk': self.object.pk})


class MemberDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a contractor member – via AJAX only."""

    model = ContractorMember

    def post(self, request, *args, **kwargs):
        member = self.get_object()
        contractor_pk = member.contractor.pk
        member.delete()
        return JsonResponse({
            'success': True,
            'message': 'Membro excluído com sucesso!',
            'redirect': str(reverse_lazy('contractors:detail', kwargs={'pk': contractor_pk}))
        })

    def get(self, request, *args, **kwargs):
        member = self.get_object()
        return HttpResponseRedirect(reverse_lazy('contractors:member_detail', kwargs={'pk': member.pk}))



class ContractorListView(LoginRequiredMixin, ListView):
    """List all contractors with search and pagination."""

    model = Contractor
    template_name = 'contractors/contractor_list.html'
    context_object_name = 'contractors'
    paginate_by = 20

    def get_queryset(self):
        queryset = Contractor.objects.prefetch_related('members').all()
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(cnpj__icontains=search) |
                Q(legal_representative__icontains=search)
            )
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ContractorSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': None}
        ]
        return context


class ContractorDetailView(LoginRequiredMixin, DetailView):
    """Display contractor details and members."""

    model = Contractor
    template_name = 'contractors/contractor_detail.html'
    context_object_name = 'contractor'

    def get_queryset(self):
        return Contractor.objects.prefetch_related('members', 'created_by', 'updated_by')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': self.object.name, 'url': None}
        ]
        return context


class ContractorCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new contractor with members."""

    model = Contractor
    form_class = ContractorForm
    template_name = 'contractors/contractor_form.html'
    success_message = "Empreiteira %(name)s criada com sucesso!"

    def get_success_url(self):
        return reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': 'Nova Empreiteira', 'url': None}
        ]
        context['form_title'] = 'Nova Empreiteira'
        context['submit_text'] = 'Criar Empreiteira'
        return context

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ContractorUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing contractor and its members."""

    model = Contractor
    form_class = ContractorForm
    template_name = 'contractors/contractor_form.html'
    success_message = "Empreiteira %(name)s atualizada com sucesso!"

    def get_success_url(self):
        return reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': self.object.name, 'url': reverse_lazy('contractors:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Empreiteira: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ContractorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a contractor – via AJAX only."""

    model = Contractor
    success_url = reverse_lazy('contractors:list')
    success_message = "Empreiteira excluída com sucesso!"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True, 'message': self.success_message})

    def get(self, request, *args, **kwargs):
        contractor = self.get_object()
        return HttpResponseRedirect(reverse_lazy('contractors:detail', kwargs={'pk': contractor.pk}))
