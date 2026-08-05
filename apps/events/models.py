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

    setup_date = models.DateField(
        'Data de Montagem (início)',
        null=True,
        blank=True
    )

    setup_date_end = models.DateField(
        'Data de Montagem (término)',
        null=True,
        blank=True
    )

    event_date_end = models.DateField(
        'Data do Evento (término)',
        null=True,
        blank=True
    )

    teardown_date = models.DateField(
        'Data de Desmontagem (início)',
        null=True,
        blank=True
    )

    teardown_date_end = models.DateField(
        'Data de Desmontagem (término)',
        null=True,
        blank=True
    )

    location = models.CharField(
        'Local',
        max_length=255,
        blank=True,
        null=True,
    )

    address = models.CharField(
        'Endereço',
        max_length=300,
        blank=True,
        null=True,
    )
    address_number = models.CharField(
        'Nº',
        max_length=20,
        blank=True,
        null=True,
    )
    address_complement = models.CharField(
        'Complemento',
        max_length=200,
        blank=True,
        null=True,
    )
    address_neighborhood = models.CharField(
        'Bairro',
        max_length=100,
        blank=True,
        null=True,
    )
    address_city = models.CharField(
        'Cidade',
        max_length=100,
        blank=True,
        null=True,
    )
    address_state = models.CharField(
        'UF',
        max_length=2,
        blank=True,
        null=True,
    )
    address_zip = models.CharField(
        'CEP',
        max_length=10,
        blank=True,
        null=True,
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

    def format_full_address(self):
        """Build a readable address from structured fields, falling back to location."""
        if self.address:
            line1 = self.address.strip()
            if self.address_number:
                line1 = f'{line1}, {self.address_number.strip()}'
            parts = [line1]
            if self.address_complement:
                parts.append(self.address_complement.strip())
            city_line = self.address_neighborhood or ''
            if self.address_city:
                city_line = f'{city_line} - {self.address_city}'.strip(' -')
            if self.address_state:
                city_line = f'{city_line}/{self.address_state}'.strip('/')
            if city_line:
                parts.append(city_line)
            if self.address_zip:
                parts.append(f'CEP {self.address_zip.strip()}')
            return ' — '.join(p for p in parts if p)
        return self.location or ''

    @property
    def display_location(self):
        return self.format_full_address() or '—'
    
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
        if hasattr(self, 'projects'):
            for project in self.projects.all():
                if project.budgets.filter(status='approved').exists():
                    return 'approved'
        
        # Check if has projects
        if hasattr(self, 'projects') and self.projects.exists():
            return 'proposal_sent'
        
        return 'planning'
