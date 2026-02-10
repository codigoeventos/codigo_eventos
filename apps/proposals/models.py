"""
Proposal model for event proposals.
"""

from django.db import models
from django.db.models import Sum
from apps.common.models import BaseModel
from apps.common.utils import get_upload_path


def proposal_upload_path(instance, filename):
    """Dynamic upload path for proposal documents."""
    return get_upload_path(instance, filename, subfolder='proposals')


class Proposal(BaseModel):
    """
    Proposal model representing commercial proposals for events.
    
    A proposal can have multiple budgets attached to it.
    """
    
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('sent', 'Enviada'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    ]
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='proposals',
        verbose_name='Evento'
    )
    
    title = models.CharField(
        'Título',
        max_length=255
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        null=True
    )
    
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    original_document = models.FileField(
        'Documento Original',
        upload_to=proposal_upload_path,
        max_length=255,
        blank=True,
        null=True,
        help_text='PDF ou DOC da proposta original'
    )
    
    class Meta:
        verbose_name = 'Proposta'
        verbose_name_plural = 'Propostas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.event.name}"
    
    @property
    def total_value(self):
        """Calculate total value from all related budgets."""
        return self.budgets.aggregate(
            total=Sum('items__total_price')
        )['total'] or 0
