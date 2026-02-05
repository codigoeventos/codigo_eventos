"""
Event Document models for file management.
"""

from django.db import models


def event_document_upload_path(instance, filename):
    """Dynamic upload path based on event ID."""
    return f"events/event_{instance.event.id}/documents/{filename}"


class EventDocument(models.Model):
    """
    Document attached to an event.
    
    Supports various document types like ART, insurance certificates, etc.
    """
    
    DOCUMENT_TYPE_CHOICES = [
        ('art', 'ART (Anotação de Responsabilidade Técnica)'),
        ('insurance', 'Seguro'),
        ('certificate', 'Certificado'),
        ('contract', 'Contrato'),
        ('other', 'Outro'),
    ]
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name='Evento'
    )
    
    file = models.FileField(
        'Arquivo',
        upload_to=event_document_upload_path
    )
    
    doc_type = models.CharField(
        'Tipo de Documento',
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES
    )
    
    description = models.CharField(
        'Descrição',
        max_length=255,
        blank=True,
        null=True
    )
    
    uploaded_at = models.DateTimeField(
        'Enviado em',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Documento do Evento'
        verbose_name_plural = 'Documentos dos Eventos'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.event.name}"
