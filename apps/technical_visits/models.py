"""
Technical Visit models for site inspection and planning.
"""

from django.db import models
from apps.common.models import BaseModel
from apps.common.utils import get_upload_path


def visit_attachment_upload_path(instance, filename):
    """Dynamic upload path for visit attachments."""
    return get_upload_path(instance, filename, subfolder='technical_visits')


class TechnicalVisit(BaseModel):
    """
    Technical Visit model for site inspections before events.
    
    Allows teams to schedule and document site visits with photos and notes.
    """
    
    STATUS_CHOICES = [
        ('scheduled', 'Agendada'),
        ('completed', 'Realizada'),
        ('cancelled', 'Cancelada'),
    ]
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='technical_visits',
        verbose_name='Evento'
    )
    
    responsible = models.ForeignKey(
        'contractors.ContractorMember',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technical_visits',
        verbose_name='Responsável'
    )
    
    visit_date = models.DateTimeField(
        'Data da Visita'
    )
    
    notes = models.TextField(
        'Observações',
        blank=True,
        null=True
    )
    
    status = models.CharField(
        'Status',
        max_length=10,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    
    class Meta:
        verbose_name = 'Visita Técnica'
        verbose_name_plural = 'Visitas Técnicas'
        ordering = ['-visit_date']
    
    def __str__(self):
        return f"Visita - {self.event.name} - {self.visit_date.strftime('%d/%m/%Y')}"


class TechnicalVisitAttachment(models.Model):
    """
    Attachments for technical visits (photos, PDFs, etc.).
    """
    
    visit = models.ForeignKey(
        'TechnicalVisit',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Visita'
    )
    
    file = models.FileField(
        'Arquivo',
        upload_to=visit_attachment_upload_path
    )
    
    uploaded_at = models.DateTimeField(
        'Enviado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Anexo da Visita Técnica'
        verbose_name_plural = 'Anexos das Visitas Técnicas'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Anexo - {self.visit}"
