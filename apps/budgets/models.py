"""
Budget models for event cost estimation.
"""

from django.db import models
from django.db.models import Sum
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
        'proposals.Proposal',
        on_delete=models.CASCADE,
        related_name='budgets',
        verbose_name='Proposta'
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
    
    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.proposal.title}"
    
    @property
    def total_value(self):
        """Calculate total value from all budget items."""
        total = self.items.aggregate(total=Sum('total_price'))['total']
        return total or 0


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
        default=1
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
    
    class Meta:
        verbose_name = 'Item do Orçamento'
        verbose_name_plural = 'Itens do Orçamento'
        ordering = ['budget', 'id']
    
    def __str__(self):
        return f"{self.name} - {self.budget.name}"
    
    def save(self, *args, **kwargs):
        """Auto-calculate total_price before saving."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
