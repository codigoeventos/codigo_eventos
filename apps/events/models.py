"""
Event model - the aggregate root of the Event Management System.
"""

from django.db import models
from apps.common.models import BaseModel


class Event(BaseModel):
    """
    Event model representing the core aggregate root.
    
    All other operational entities (proposals, budgets, service orders, etc.)
    are linked to an event.
    """
    
    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.PROTECT,
        related_name='events',
        verbose_name='Cliente'
    )
    
    name = models.CharField(
        'Nome do Evento',
        max_length=255
    )
    
    event_date = models.DateField(
        'Data do Evento'
    )
    
    location = models.CharField(
        'Local',
        max_length=255
    )
    
    notes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.name} - {self.event_date.strftime('%d/%m/%Y')}"
    
    @property
    def status(self):
        """
        Calculate event status based on related entities.
        """
        # Check if has approved service order
        if hasattr(self, 'service_orders') and self.service_orders.filter(status='completed').exists():
            return 'completed'
        
        if hasattr(self, 'service_orders') and self.service_orders.filter(status='in_progress').exists():
            return 'in_progress'
        
        # Check if has approved budget
        if hasattr(self, 'proposals'):
            for proposal in self.proposals.all():
                if proposal.budgets.filter(status='approved').exists():
                    return 'approved'
        
        # Check if has proposals
        if hasattr(self, 'proposals') and self.proposals.exists():
            return 'proposal_sent'
        
        return 'planning'
