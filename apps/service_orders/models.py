"""
Service Order models for event execution tracking.
"""

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
    
    class Meta:
        verbose_name = 'Ordem de Serviço'
        verbose_name_plural = 'Ordens de Serviço'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OS {self.pk} - {self.event.name}"


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
    
    execution_status = models.CharField(
        'Status de Execução',
        max_length=15,
        choices=EXECUTION_STATUS_CHOICES,
        default='pending'
    )
    
    class Meta:
        verbose_name = 'Item da Ordem de Serviço'
        verbose_name_plural = 'Itens da Ordem de Serviço'
        ordering = ['service_order', 'id']
    
    def __str__(self):
        return f"{self.name} - OS {self.service_order.pk}"
