"""
ART (Anotação de Responsabilidade Técnica) model.
"""

import uuid
import os
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.conf import settings

from apps.common.models import BaseModel
from apps.common.utils import get_upload_path


def art_file_upload_path(instance, filename):
    """Dynamic upload path for ART files."""
    return get_upload_path(instance, filename, subfolder='art_files')


class ART(BaseModel):
    """
    ART – Anotação de Responsabilidade Técnica.

    Document generated for the engineer in charge of the project.
    Linked to a Service Order.
    The quantity is auto-calculated as the sum of all budget items' measurement.
    """

    service_order = models.OneToOneField(
        'service_orders.ServiceOrder',
        on_delete=models.PROTECT,
        related_name='art',
        verbose_name='Ordem de Serviço',
    )

    public_token = models.UUIDField(
        'Token Público',
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text='Token único para link público de visualização da ART',
    )

    # ── Engenheiro ────────────────────────────────────────────────────────
    engineer_name = models.CharField(
        'Nome do Engenheiro',
        max_length=255,
        blank=True,
        null=True,
        help_text='Preenchido manualmente no documento PDF',
    )

    engineer_crea = models.CharField(
        'CREA do Engenheiro',
        max_length=50,
        blank=True,
        null=True,
        help_text='Número de registro no CREA',
    )

    # ── Serviço ───────────────────────────────────────────────────────────
    # ── Contratado – nome e doc ───────────────────────────────────────────
    contratante_nome = models.CharField('Nome do Contratante', max_length=255, blank=True, null=True)
    contratante_cnpj = models.CharField('CNPJ do Contratante', max_length=18, blank=True, null=True)

    # ── Contratado – endereço ─────────────────────────────────────────────
    client_address = models.CharField('Endereço (Contratado)', max_length=300, blank=True, null=True)
    client_number  = models.CharField('N° (Contratado)',       max_length=20,  blank=True, null=True)
    client_complement = models.CharField('Complemento (Contratado)', max_length=100, blank=True, null=True)
    client_neighborhood = models.CharField('Bairro (Contratado)', max_length=100, blank=True, null=True)
    client_city    = models.CharField('Cidade (Contratado)',    max_length=100, blank=True, null=True)
    client_state   = models.CharField('UF (Contratado)',        max_length=2,   blank=True, null=True)
    client_zip     = models.CharField('CEP (Contratado)',       max_length=10,  blank=True, null=True)

    TIPO_CONTRATANTE_CHOICES = [
        ('pf_privado',  'Pessoa Física de Direito Privado'),
        ('pj_privado',  'Pessoa Jurídica de Direito Privado'),
        ('pf_publico',  'Pessoa Física de Direito Público'),
        ('pj_publico',  'Pessoa Jurídica de Direito Público'),
    ]
    tipo_contratante = models.CharField(
        'Tipo de Contratante',
        max_length=20,
        choices=TIPO_CONTRATANTE_CHOICES,
        blank=True,
        null=True,
    )

    # ── Obra / Serviço – endereço ─────────────────────────────────────────
    obra_address    = models.CharField('Endereço (Obra)',    max_length=300, blank=True, null=True)
    obra_number     = models.CharField('N° (Obra)',          max_length=20,  blank=True, null=True)
    obra_complement = models.CharField('Complemento (Obra)', max_length=200, blank=True, null=True)
    obra_neighborhood= models.CharField('Bairro (Obra)',     max_length=100, blank=True, null=True)
    obra_city       = models.CharField('Cidade (Obra)',      max_length=100, blank=True, null=True)
    obra_state      = models.CharField('UF (Obra)',          max_length=2,   blank=True, null=True)
    obra_zip        = models.CharField('CEP (Obra)',         max_length=10,  blank=True, null=True)

    # ── Atividades técnicas ───────────────────────────────────────────────
    nivel_atuacao   = models.CharField('Nível de Atuação',        max_length=100, blank=True, null=True)
    atividade       = models.CharField('Atividade',               max_length=100, blank=True, null=True)
    atividade_complemento = models.CharField('Complemento da Atividade', max_length=200, blank=True, null=True)
    obra_servico    = models.CharField('Obra / Serviço',          max_length=200, blank=True, null=True)

    activity_description = models.TextField(
        'Descrição da Atividade / Serviço',
        blank=True,
        null=True,
        help_text='Objeto técnico da contratação',
    )

    location = models.CharField(
        'Local da Obra / Endereço (legado)',
        max_length=500,
        blank=True,
        null=True,
    )

    # ── Quantidade (metragem total do orçamento) ──────────────────────────
    quantity = models.DecimalField(
        'Quantidade Total',
        max_digits=12,
        decimal_places=3,
        help_text='Soma da metragem dos itens do orçamento',
    )

    MEASUREMENT_UNIT_CHOICES = [
        ('m', 'metros (m)'),
        ('m2', 'metros² (m²)'),
        ('m3', 'metros³ (m³)'),
        ('un', 'unidades (un)'),
    ]

    measurement_unit = models.CharField(
        'Unidade de Medida',
        max_length=10,
        choices=MEASUREMENT_UNIT_CHOICES,
        default='m3',
    )

    # ── Contrato / Prazo ──────────────────────────────────────────────────
    contract_value = models.DecimalField(
        'Valor do Contrato (R$)',
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        'Data de Início',
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        'Data de Conclusão',
        null=True,
        blank=True,
    )

    # ── Observações ───────────────────────────────────────────────────────
    notes = models.TextField(
        'Observações',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'ART'
        verbose_name_plural = 'ARTs'
        ordering = ['-created_at']

    def __str__(self):
        os_label = f"OS #{self.service_order_id}" if self.service_order_id else 'Sem OS'
        return f"ART {self.pk} – {os_label}"

    def get_public_url(self):
        """Return the public share URL for this ART."""
        return reverse('art:public', kwargs={'token': str(self.public_token)})

    def get_absolute_url(self):
        return reverse('art:detail', kwargs={'pk': self.pk})

    # ── Helpers ───────────────────────────────────────────────────────────
    @property
    def art_number(self):
        """Formatted ART number like ART-0001."""
        return f"ART-{self.pk:04d}"

    @classmethod
    def calculate_quantity(cls, service_order):
        """Return the sum of measurement of all items in the service order budget."""
        from apps.budgets.models import BudgetItem
        if not service_order or not service_order.budget_id:
            return Decimal('0')
        result = (
            BudgetItem.objects
            .filter(budget_id=service_order.budget_id, measurement__isnull=False)
            .aggregate(total=models.Sum('measurement'))['total']
        )
        return result or Decimal('0')

    @classmethod
    def build_initial_data(cls, service_order):
        """Build default values for ART fields from service order/budget/project data."""
        if not service_order or not service_order.budget_id:
            return {
                'quantity': Decimal('0'),
                'measurement_unit': 'm3',
            }

        budget = service_order.budget
        project = budget.proposal
        event = project.event if project else None
        client = event.client if event else None

        quantity = cls.calculate_quantity(service_order) or Decimal('0')

        activity_parts = [budget.name]
        if project and project.title and project.title != budget.name:
            activity_parts.append(project.title)
        if project and project.description:
            activity_parts.append(project.description)

        atividade = budget.name or (project.title if project else '') or (event.name if event else '')
        obra_servico = (project.title if project and project.title else '') or (event.name if event else '') or budget.name
        atividade_complemento = event.location if event and event.location else ''

        tipo_contratante = None
        if client and client.document_type == 'cpf':
            tipo_contratante = 'pf_privado'
        elif client and client.document_type == 'cnpj':
            tipo_contratante = 'pj_privado'

        contratante_nome = client.name if client else ''
        contratante_cnpj = client.document_number if client and client.document_type == 'cnpj' else ''

        return {
            'engineer_name': '',
            'engineer_crea': '',
            'contratante_nome': contratante_nome,
            'contratante_cnpj': contratante_cnpj,
            'client_address': '',
            'client_number': '',
            'client_complement': '',
            'client_neighborhood': '',
            'client_city': '',
            'client_state': '',
            'client_zip': '',
            'tipo_contratante': tipo_contratante,
            'obra_address': event.location if event else '',
            'obra_number': '',
            'obra_complement': '',
            'obra_neighborhood': '',
            'obra_city': '',
            'obra_state': '',
            'obra_zip': '',
            'nivel_atuacao': 'Execução',
            'atividade': atividade,
            'atividade_complemento': atividade_complemento,
            'obra_servico': obra_servico,
            'activity_description': '\n'.join(activity_parts),
            'location': event.location if event else '',
            'quantity': quantity,
            'measurement_unit': 'm3',
            'contract_value': budget.total_with_freight or Decimal('0'),
            'start_date': event.setup_date if event and event.setup_date else None,
            'end_date': event.event_date if event else None,
            'notes': '',
        }

    @property
    def project(self):
        """Compatibility accessor: project derived from linked service order budget."""
        if not self.service_order_id or not self.service_order.budget_id:
            return None
        return self.service_order.budget.proposal


class ARTFile(models.Model):
    """Additional files attached to an ART."""

    art = models.ForeignKey(
        ART,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='ART'
    )

    name = models.CharField(
        'Nome do Arquivo',
        max_length=255,
        blank=True,
        null=True,
    )

    file = models.FileField(
        'Arquivo',
        upload_to=art_file_upload_path,
        max_length=500,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Enviado em')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Enviado por',
    )

    class Meta:
        verbose_name = 'Arquivo de ART'
        verbose_name_plural = 'Arquivos de ART'
        ordering = ['-uploaded_at']

    def __str__(self):
        label = self.name or self.filename
        return f"{label} — {self.art.art_number}"

    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else ''
