"""
Budget models for event cost estimation.
"""

import uuid
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from apps.common.models import BaseModel


class Budget(BaseModel):
    """
    Budget model representing a cost estimate for an event proposal.
    
    Contains multiple budget items with calculated totals.
    When approved, automatically generates a Service Order.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('sent', 'Enviado'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    proposal = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='budgets',
        verbose_name='Projeto'
    )
    
    name = models.CharField(
        'Nome',
        max_length=255,
        help_text='Nome identificador deste orçamento'
    )
    
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    is_selected = models.BooleanField(
        'Selecionado',
        default=False,
        help_text='Orçamento escolhido pelo cliente'
    )
    
    approval_token = models.UUIDField(
        'Token de Aprovação',
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text='Token único para link público de aprovação'
    )
    
    approval_status = models.CharField(
        'Status de Aprovação',
        max_length=20,
        choices=[
            ('pending', 'Pendente'),
            ('approved', 'Aprovado pelo Cliente'),
            ('rejected', 'Rejeitado pelo Cliente'),
        ],
        default='pending'
    )
    
    approved_at = models.DateTimeField(
        'Data de Aprovação',
        blank=True,
        null=True
    )
    
    client_notes = models.TextField(
        'Observações do Cliente',
        blank=True,
        null=True,
        help_text='Comentários do cliente na aprovação'
    )

    # ── Logistics / Freight ──────────────────────────────────────────────
    freight_cost = models.DecimalField(
        'Custo de Frete (R$)',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Calculado automaticamente ou informado manualmente'
    )
    freight_urgency = models.ForeignKey(
        'logistics.UrgencyMultiplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='budgets',
        verbose_name='Urgência de Entrega'
    )
    freight_distance_km = models.DecimalField(
        'Distância para Entrega (km)',
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Usado no cálculo por distância (opcional)'
    )

    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.proposal.title}"
    
    def get_approval_url(self):
        """Generate public approval URL."""
        from django.urls import reverse
        return reverse('budgets:public_approval', kwargs={'token': str(self.approval_token)})
    
    @property
    def total_value(self):
        """Calculate total value from all budget items."""
        total = self.items.aggregate(total=Sum('total_price'))['total']
        return total or 0
    
    @property
    def approved_value(self):
        """Calculate total value from approved items only."""
        total = self.items.filter(is_approved=True).aggregate(total=Sum('total_price'))['total']
        return total or 0
    
    @property
    def is_editable(self):
        """Check if budget can still be edited."""
        return self.approval_status == 'pending'

    @property
    def total_with_freight(self):
        """Budget total value plus freight cost."""
        freight = self.freight_cost or 0
        return self.total_value + freight

    @property
    def total_weight(self):
        """Sum of (weight × quantity) across all items that have weight."""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.items.all():
            if item.weight:
                total += item.weight * item.quantity
        return total

    @property
    def total_volume(self):
        """Sum of (measurement × quantity) for items with measurement_unit == 'm3'."""
        from decimal import Decimal
        total = Decimal('0')
        for item in self.items.all():
            if item.measurement and item.measurement_unit == 'm3':
                total += item.measurement * item.quantity
        return total


class BudgetItem(models.Model):
    """
    Individual line item in a budget.
    
    Auto-calculates total_price from quantity * unit_price.
    """
    
    budget = models.ForeignKey(
        'Budget',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Orçamento'
    )
    
    name = models.CharField(
        'Item',
        max_length=255
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        null=True
    )
    
    quantity = models.IntegerField(
        'Quantidade',
        default=1,
        help_text='Quantidade de unidades'
    )
    
    measurement = models.DecimalField(
        'Metragem / Volume (m³)',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Preenchido automaticamente a partir das dimensões, ou manualmente'
    )

    measurement_unit = models.CharField(
        'Unidade de Medida',
        max_length=10,
        blank=True,
        null=True,
        choices=[
            ('m', 'metros (m)'),
            ('m2', 'metros² (m²)'),
            ('m3', 'metros³ (m³)'),
        ],
        help_text='Tipo de unidade de medida'
    )

    # Dimensions for automatic volume calculation
    dim_length = models.DecimalField(
        'Comprimento (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Comprimento unitário em metros'
    )
    dim_width = models.DecimalField(
        'Largura (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Largura unitária em metros'
    )
    dim_height = models.DecimalField(
        'Altura (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Altura unitária em metros'
    )

    weight = models.DecimalField(
        'Peso Unitário (kg)',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
        help_text='Peso por unidade em quilogramas'
    )
    
    unit_price = models.DecimalField(
        'Preço Unitário',
        max_digits=10,
        decimal_places=2
    )
    
    total_price = models.DecimalField(
        'Preço Total',
        max_digits=10,
        decimal_places=2,
        editable=False
    )
    
    is_approved = models.BooleanField(
        'Aprovado pelo Cliente',
        default=True,
        help_text='Item selecionado para aprovação pelo cliente'
    )
    
    class Meta:
        verbose_name = 'Item do Orçamento'
        verbose_name_plural = 'Itens do Orçamento'
        ordering = ['budget', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.budget.name}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total_price and volume before saving."""
        # If all three dimensions are provided, compute volume (m³) automatically
        if self.dim_length and self.dim_width and self.dim_height:
            self.measurement = self.dim_length * self.dim_width * self.dim_height
            self.measurement_unit = 'm3'
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
