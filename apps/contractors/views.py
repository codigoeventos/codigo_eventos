"""
Contractor views for Event Management System.
"""

import re
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views import View
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

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


class CNPJLookupView(LoginRequiredMixin, View):
    """API endpoint to lookup CNPJ data from ReceitaWS."""
    
    def get(self, request, *args, **kwargs):
        cnpj = request.GET.get('cnpj', '').strip()
        
        # Remove formatação do CNPJ (pontos, barras, hífens)
        cnpj_clean = ''.join(filter(str.isdigit, cnpj))
        
        if len(cnpj_clean) != 14:
            return JsonResponse({
                'success': False,
                'error': 'CNPJ inválido. Deve conter 14 dígitos.'
            }, status=400)
        
        try:
            # Consulta à API da ReceitaWS
            response = requests.get(
                f'https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}',
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se houve erro na consulta
                if data.get('status') == 'ERROR':
                    return JsonResponse({
                        'success': False,
                        'error': data.get('message', 'Erro ao consultar CNPJ')
                    }, status=400)
                
                # Formata os dados para retornar
                return JsonResponse({
                    'success': True,
                    'data': {
                        'name': data.get('nome', ''),
                        'trade_name': data.get('fantasia', ''),
                        'phone': data.get('telefone', ''),
                        'email': data.get('email', ''),
                        'address_street': data.get('logradouro', ''),
                        'address_number': data.get('numero', ''),
                        'address_complement': data.get('complemento', ''),
                        'address_neighborhood': data.get('bairro', ''),
                        'address_city': data.get('municipio', ''),
                        'address_state': data.get('uf', ''),
                        'address_zip': data.get('cep', ''),
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Erro ao consultar CNPJ. Tente novamente.'
                }, status=response.status_code)
                
        except requests.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'Timeout ao consultar CNPJ. Tente novamente.'
            }, status=408)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erro ao consultar CNPJ: {str(e)}'
            }, status=500)






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
        members = list(self.object.members.all())
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': self.object.name, 'url': None}
        ]
        context['blocked_members_count'] = sum(1 for m in members if m.is_blocked_from_events)
        context['expiring_members_count'] = sum(1 for m in members if m.worst_doc_status == 'expiring_soon')
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


# ---------------------------------------------------------------------------
# Documentation Report  (feature 4.4)
# ---------------------------------------------------------------------------

class DocumentationReportView(LoginRequiredMixin, TemplateView):
    """
    Report listing all ContractorMembers with their NR / ASO document status.
    Filterable by ?status=all|expired|expiring_soon|valid|no_doc
    """
    template_name = 'contractors/doc_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        status_filter = self.request.GET.get('status', 'all')

        qs = ContractorMember.objects.select_related('contractor').order_by('contractor__name', 'name')
        members = list(qs)

        VALID_FILTERS = ('expired', 'expiring_soon', 'valid', 'no_doc')

        def _matches(m):
            if status_filter not in VALID_FILTERS:
                return True
            return m.worst_doc_status == status_filter

        members = [m for m in members if _matches(m)]

        # Summary counts from full queryset
        all_members = list(ContractorMember.objects.select_related('contractor'))
        counts = {
            'total':         len(all_members),
            'expired':       sum(1 for m in all_members if m.worst_doc_status == 'expired'),
            'expiring_soon': sum(1 for m in all_members if m.worst_doc_status == 'expiring_soon'),
            'valid':         sum(1 for m in all_members if m.worst_doc_status == 'valid'),
            'no_doc':        sum(1 for m in all_members if m.worst_doc_status == 'no_doc'),
        }

        context['members'] = members
        context['counts'] = counts
        context['status_filter'] = status_filter
        context['today'] = today
        context['breadcrumbs'] = [
            {'name': 'Empreiteiras', 'url': reverse_lazy('contractors:list')},
            {'name': 'Relatório de Documentação', 'url': None},
        ]
        return context
