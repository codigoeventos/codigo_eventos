"""
ART (Anotação de Responsabilidade Técnica) views.
"""

from decimal import Decimal
from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView

from apps.service_orders.models import ServiceOrder
from .models import ART, ARTFile
from .forms import ARTEditForm


class ARTGenerateView(LoginRequiredMixin, View):
    """
    Generates an ART automatically from service order data.

    GET  → confirmation page showing what will be generated.
    POST → creates the ART and redirects to the detail page.

    Rules:
    - Only one ART per service order (OneToOne). If one already exists, redirect to it.
    - All data is derived automatically; no manual form required.
    """

    def _get_service_order(self, pk):
        return get_object_or_404(
            ServiceOrder.objects.select_related('budget', 'budget__proposal', 'budget__proposal__event', 'budget__proposal__event__client', 'event', 'event__client'),
            pk=pk,
        )

    def _guard(self, request, service_order):
        """Return a redirect response if ART cannot be created, else None."""
        existing = ART.objects.filter(service_order=service_order).first()
        if existing:
            messages.info(request, 'Esta OS já possui uma ART.')
            return redirect('art:detail', pk=existing.pk)
        return None

    def _parse_decimal(self, raw_value, default):
        if raw_value is None:
            return default
        value = str(raw_value).strip()
        if value == '':
            return default
        normalized = value
        if ',' in normalized:
            normalized = normalized.replace('.', '').replace(',', '.')
        try:
            return Decimal(normalized)
        except Exception:
            return default

    def _parse_date(self, raw_value, default):
        if raw_value is None:
            return default
        value = str(raw_value).strip()
        if value == '':
            return None
        try:
            return date.fromisoformat(value)
        except Exception:
            return default

    def _build_art_data(self, request, service_order):
        """Build ART data from defaults + popup form input."""
        defaults = ART.build_initial_data(service_order)

        text_fields = [
            'engineer_name', 'engineer_crea',
            'client_address', 'client_number', 'client_complement',
            'client_neighborhood', 'client_city', 'client_state', 'client_zip',
            'obra_address', 'obra_number', 'obra_complement',
            'obra_neighborhood', 'obra_city', 'obra_state', 'obra_zip',
            'notes',
        ]

        data = defaults.copy()

        # Technical activity fields are always backend-driven.
        last_art = ART.all_objects.filter(service_order=service_order).order_by('-updated_at', '-created_at').first()
        if last_art:
            for field in ['nivel_atuacao', 'atividade', 'atividade_complemento', 'obra_servico', 'activity_description']:
                value = getattr(last_art, field, None)
                if value not in (None, ''):
                    data[field] = value

        for field in text_fields:
            if field in request.POST:
                data[field] = request.POST.get(field, '').strip()

        tipo_contratante = request.POST.get('tipo_contratante')
        if tipo_contratante in dict(ART.TIPO_CONTRATANTE_CHOICES):
            data['tipo_contratante'] = tipo_contratante

        measurement_unit = request.POST.get('measurement_unit')
        if measurement_unit in dict(ART.MEASUREMENT_UNIT_CHOICES):
            data['measurement_unit'] = measurement_unit

        data['quantity'] = self._parse_decimal(request.POST.get('quantity'), defaults.get('quantity', Decimal('0')))
        data['contract_value'] = self._parse_decimal(request.POST.get('contract_value'), defaults.get('contract_value'))
        data['start_date'] = self._parse_date(request.POST.get('start_date'), defaults.get('start_date'))
        data['end_date'] = self._parse_date(request.POST.get('end_date'), defaults.get('end_date'))
        data['location'] = data.get('obra_address') or defaults.get('location', '')

        return data

    def post(self, request, service_order_pk):
        service_order = self._get_service_order(service_order_pk)
        guard = self._guard(request, service_order)
        if guard:
            return guard

        data = self._build_art_data(request, service_order)

        # If a soft-deleted ART already exists for this service order, restore and
        # update it instead of creating a new one (avoids UniqueConstraint error).
        deleted_art = ART.all_objects.filter(service_order=service_order).first()
        if deleted_art:
            deleted_art.undelete()
            deleted_art.engineer_name = data.get('engineer_name')
            deleted_art.engineer_crea = data.get('engineer_crea')
            deleted_art.client_address = data.get('client_address')
            deleted_art.client_number = data.get('client_number')
            deleted_art.client_complement = data.get('client_complement')
            deleted_art.client_neighborhood = data.get('client_neighborhood')
            deleted_art.client_city = data.get('client_city')
            deleted_art.client_state = data.get('client_state')
            deleted_art.client_zip = data.get('client_zip')
            deleted_art.tipo_contratante = data.get('tipo_contratante')
            deleted_art.obra_address = data.get('obra_address')
            deleted_art.obra_number = data.get('obra_number')
            deleted_art.obra_complement = data.get('obra_complement')
            deleted_art.obra_neighborhood = data.get('obra_neighborhood')
            deleted_art.obra_city = data.get('obra_city')
            deleted_art.obra_state = data.get('obra_state')
            deleted_art.obra_zip = data.get('obra_zip')
            deleted_art.nivel_atuacao = data.get('nivel_atuacao')
            deleted_art.atividade = data.get('atividade')
            deleted_art.atividade_complemento = data.get('atividade_complemento')
            deleted_art.obra_servico = data.get('obra_servico')
            deleted_art.activity_description = data.get('activity_description')
            deleted_art.notes = data.get('notes')
            deleted_art.location = data.get('location')
            deleted_art.quantity = data.get('quantity')
            deleted_art.measurement_unit = data.get('measurement_unit') or 'm3'
            deleted_art.contract_value = data.get('contract_value') if data.get('contract_value') else None
            deleted_art.start_date = data.get('start_date')
            deleted_art.end_date = data.get('end_date')
            deleted_art.updated_by = request.user
            deleted_art.save()
            art = deleted_art
        else:
            art = ART.objects.create(
                service_order=service_order,
                engineer_name=data.get('engineer_name'),
                engineer_crea=data.get('engineer_crea'),
                client_address=data.get('client_address'),
                client_number=data.get('client_number'),
                client_complement=data.get('client_complement'),
                client_neighborhood=data.get('client_neighborhood'),
                client_city=data.get('client_city'),
                client_state=data.get('client_state'),
                client_zip=data.get('client_zip'),
                tipo_contratante=data.get('tipo_contratante'),
                obra_address=data.get('obra_address'),
                obra_number=data.get('obra_number'),
                obra_complement=data.get('obra_complement'),
                obra_neighborhood=data.get('obra_neighborhood'),
                obra_city=data.get('obra_city'),
                obra_state=data.get('obra_state'),
                obra_zip=data.get('obra_zip'),
                nivel_atuacao=data.get('nivel_atuacao'),
                atividade=data.get('atividade'),
                atividade_complemento=data.get('atividade_complemento'),
                obra_servico=data.get('obra_servico'),
                activity_description=data.get('activity_description'),
                notes=data.get('notes'),
                location=data.get('location'),
                quantity=data.get('quantity'),
                measurement_unit=data.get('measurement_unit') or 'm3',
                contract_value=data.get('contract_value') if data.get('contract_value') else None,
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                created_by=request.user,
                updated_by=request.user,
            )

        messages.success(request, f'ART {art.art_number} gerada com sucesso!')
        return redirect('art:detail', pk=art.pk)


class ARTDetailView(LoginRequiredMixin, DetailView):
    """Internal detail view for an ART (authenticated)."""

    model = ART
    template_name = 'art/art_detail.html'
    context_object_name = 'art'

    def get_queryset(self):
        return ART.objects.select_related(
            'service_order',
            'service_order__budget',
            'service_order__budget__proposal',
            'service_order__budget__proposal__event',
            'service_order__budget__proposal__event__client',
            'service_order__event',
            'service_order__event__client',
            'created_by',
            'updated_by',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': reverse_lazy('service_orders:list')},
            {'name': f'OS #{self.object.service_order.pk}', 'url': reverse_lazy('service_orders:detail', kwargs={'pk': self.object.service_order.pk})},
            {'name': self.object.art_number, 'url': None},
        ]
        return context


class PublicARTView(View):
    """
    Public (unauthenticated) view of an ART, accessible via UUID token.
    Renders a print-friendly HTML page (same pattern as OS public view).
    """

    def get(self, request, token):
        art = get_object_or_404(
            ART.objects.select_related(
                'service_order',
                'service_order__budget',
                'service_order__budget__proposal',
                'service_order__budget__proposal__event',
                'service_order__budget__proposal__event__client',
                'service_order__event',
                'service_order__event__client',
                'created_by',
            ),
            public_token=token,
        )
        return render(request, 'art/public_art.html', {
            'art': art,
        })


class ARTUpdateView(LoginRequiredMixin, UpdateView):
    """Edit engineer data and other ART fields after auto-generation."""

    model = ART
    form_class = ARTEditForm
    template_name = 'art/art_edit.html'
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Ordens de Serviço', 'url': reverse_lazy('service_orders:list')},
            {'name': f'OS #{self.object.service_order.pk}', 'url': reverse_lazy('service_orders:detail', kwargs={'pk': self.object.service_order.pk})},
            {'name': self.object.art_number, 'url': reverse_lazy('art:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None},
        ]
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'ART atualizada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('art:detail', kwargs={'pk': self.object.pk})


class ARTDeleteView(LoginRequiredMixin, View):
    """Delete an ART (redirects back to service order)."""

    def post(self, request, pk):
        art = get_object_or_404(ART, pk=pk)
        service_order_pk = art.service_order.pk
        art.delete()
        messages.success(request, 'ART excluída com sucesso.')
        return redirect('service_orders:detail', pk=service_order_pk)


class ARTFileUploadView(LoginRequiredMixin, View):
    """Upload one or more files linked to an ART."""

    def post(self, request, art_pk):
        art = get_object_or_404(ART, pk=art_pk)
        files = request.FILES.getlist('files')
        next_url = request.POST.get('next')

        if not files:
            messages.warning(request, 'Selecione ao menos um arquivo para enviar.')
            if next_url:
                return redirect(next_url)
            return redirect('service_orders:detail', pk=art.service_order.pk)

        created_count = 0
        for uploaded in files:
            ARTFile.objects.create(
                art=art,
                name=uploaded.name,
                file=uploaded,
                uploaded_by=request.user,
            )
            created_count += 1

        messages.success(request, f'{created_count} arquivo(s) enviado(s) para a ART com sucesso.')
        if next_url:
            return redirect(next_url)
        return redirect('service_orders:detail', pk=art.service_order.pk)


class ARTFileDeleteView(LoginRequiredMixin, View):
    """Delete a file linked to an ART."""

    def post(self, request, pk):
        art_file = get_object_or_404(ARTFile, pk=pk)
        service_order_pk = art_file.art.service_order.pk
        next_url = request.POST.get('next')
        art_file.delete()
        messages.success(request, 'Arquivo da ART removido com sucesso.')
        if next_url:
            return redirect(next_url)
        return redirect('service_orders:detail', pk=service_order_pk)
