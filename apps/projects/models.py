"""
Project model for event projects.
"""

import os
from django.conf import settings
from django.db import models
from django.db.models import Sum
from apps.common.models import BaseModel
from apps.common.utils import get_upload_path


def project_upload_path(instance, filename):
    """Dynamic upload path for project documents."""
    return get_upload_path(instance, filename, subfolder='projects')


def project_file_upload_path(instance, filename):
    """Dynamic upload path for project files."""
    return f'projects/{instance.project.pk}/files/{filename}'


class Project(BaseModel):
    """
    Project model representing commercial projects for events.

    A project can have multiple budgets and uploaded files attached to it.
    """

    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('in_development', 'Em Desenvolvimento'),
        ('sent', 'Enviado'),
        ('approved', 'Aprovado'),
        ('in_execution', 'Em Execução'),
        ('rejected', 'Rejeitado'),
        ('completed', 'Concluído'),
    ]

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Evento'
    )

    contractor = models.ForeignKey(
        'contractors.Contractor',
        on_delete=models.SET_NULL,
        related_name='projects',
        verbose_name='Empreiteira Responsável',
        blank=True,
        null=True,
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
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    original_document = models.FileField(
        'Documento Original',
        upload_to=project_upload_path,
        max_length=255,
        blank=True,
        null=True,
        help_text='PDF ou DOC da proposta original'
    )

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.event.name}"

    @property
    def total_value(self):
        """Calculate total value from all related budgets."""
        return self.budgets.aggregate(
            total=Sum('items__total_price')
        )['total'] or 0


class ProjectFile(models.Model):
    """Additional files attached to a project (plants, technical drawings, etc.)."""

    FILE_TYPE_CHOICES = [
        ('plant', 'Planta'),
        ('drawing', 'Desenho Técnico'),
        ('specification', 'Especificação'),
        ('contract', 'Contrato'),
        ('other', 'Outro'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Projeto'
    )

    name = models.CharField(
        'Nome do Arquivo',
        max_length=255
    )

    file = models.FileField(
        'Arquivo',
        upload_to=project_file_upload_path,
        max_length=500,
    )

    file_type = models.CharField(
        'Tipo',
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default='other'
    )

    notes = models.CharField(
        'Observações',
        max_length=500,
        blank=True,
        null=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Enviado em')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Enviado por',
    )

    class Meta:
        verbose_name = 'Arquivo de Projeto'
        verbose_name_plural = 'Arquivos de Projeto'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} — {self.project.title}"

    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else ''

    @property
    def extension(self):
        _, ext = os.path.splitext(self.filename)
        return ext.lower().lstrip('.')

    @property
    def is_image(self):
        return self.extension in ('jpg', 'jpeg', 'png', 'gif', 'webp', 'svg')

    @property
    def is_pdf(self):
        return self.extension == 'pdf'
