"""
ART (Anotação de Responsabilidade Técnica) model.
"""

import uuid
from decimal import Decimal

from django.db import models
from django.urls import reverse

from apps.common.models import BaseModel


class ART(BaseModel):
    """
    ART – Anotação de Responsabilidade Técnica.

    Document generated for the engineer in charge of the project.
    Linked to a Project and requires at least one Budget.
    The quantity is auto-calculated as the sum of all budget items' measurement.
    """

    project = models.OneToOneField(
        'projects.Project',
        on_delete=models.PROTECT,
        related_name='art',
        verbose_name='Projeto',
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
    activity_description = models.TextField(
        'Descrição da Atividade / Serviço',
        blank=True,
        null=True,
        help_text='Objeto técnico da contratação',
    )

    location = models.CharField(
        'Local da Obra / Endereço',
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
        return f"ART {self.pk} – {self.project.title}"

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
    def calculate_quantity(cls, project):
        """Return the sum of measurement of all items in the project's budgets."""
        from apps.budgets.models import BudgetItem
        result = (
            BudgetItem.objects
            .filter(budget__proposal=project, measurement__isnull=False)
            .aggregate(total=models.Sum('measurement'))['total']
        )
        return result or Decimal('0')
