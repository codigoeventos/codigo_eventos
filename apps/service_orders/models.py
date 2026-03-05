"""
Service Order models for event execution tracking.
"""

import uuid
from django.db import models
from apps.common.models import BaseModel


class ServiceOrder(BaseModel):
    """
    Service Order model representing work to be executed for an event.
    
    Automatically created when a budget is approved.
    Tracks execution status of event services.
    """
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada'),
    ]
    
    budget = models.OneToOneField(
        'budgets.Budget',
        on_delete=models.PROTECT,
        related_name='service_order',
        verbose_name='Orçamento'
    )
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='service_orders',
        verbose_name='Evento'
    )
    
    status = models.CharField(
        'Status',
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )

    public_token = models.UUIDField(
        'Token Público',
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text='Token único para link público de visualização da OS'
    )

    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OS {self.pk} - {self.event.name}"

    def get_public_url(self):
        """Generate public share URL for this service order."""
        from django.urls import reverse
        return reverse('service_orders:public', kwargs={'token': str(self.public_token)})


class ServiceOrderItem(models.Model):
    """
    Individual task in a service order.
    
    Broken down from budget items for granular execution tracking.
    """
    
    EXECUTION_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
    ]
    
    service_order = models.ForeignKey(
        'ServiceOrder',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Ordem de Serviço'
    )

    budget_item = models.OneToOneField(
        'budgets.BudgetItem',
        on_delete=models.SET_NULL,
        related_name='service_order_item',
        verbose_name='Item do Orçamento',
        null=True,
        blank=True,
        help_text='Item do orçamento de origem (rastreabilidade)'
    )

    section_name = models.CharField(
        'Seção',
        max_length=255,
        blank=True,
        null=True,
        help_text='Nome da seção de agrupamento (copiado do orçamento)'
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

    # ── Dimensões e Logística (copiados do orçamento, sem preços) ─────────
    dim_length = models.DecimalField(
        'Comprimento (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
    )
    dim_width = models.DecimalField(
        'Largura (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
    )
    dim_height = models.DecimalField(
        'Altura (m)',
        max_digits=8,
        decimal_places=3,
        blank=True,
        null=True,
    )
    measurement = models.DecimalField(
        'Metragem / Volume (m³)',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
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
    )
    weight = models.DecimalField(
        'Peso Unitário (kg)',
        max_digits=10,
        decimal_places=3,
        blank=True,
        null=True,
    )

    execution_status = models.CharField(
        'Status de Execução',
        max_length=15,
        choices=EXECUTION_STATUS_CHOICES,
        default='pending'
    )
    
    class Meta:
        verbose_name = 'Item da Ordem de Serviço'
        verbose_name_plural = 'Itens da Ordem de Serviço'
        ordering = ['service_order', 'section_name', 'id']
    
    def __str__(self):
        return f"{self.name} - OS {self.service_order.pk}"
