"""
Base models for the Event Management System.

Provides audit trail and soft delete functionality for all domain models.
"""

from django.db import models
from django.conf import settings
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
from simple_history.models import HistoricalRecords


class BaseModel(SafeDeleteModel):
    """
    Abstract base model with audit trail and soft delete.
    
    All domain models should inherit from this to get:
    - created_at, updated_at timestamps
    - created_by, updated_by user tracking
    - Soft delete functionality (deleted items hidden by default)
    - Historical records for audit trail
    """
    
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name='Criado por'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name='Atualizado por'
    )
    
    history = HistoricalRecords(inherit=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
        
    def save(self, *args, **kwargs):
        """Override save to handle user tracking."""
        # The user will be set via view mixins
        super().save(*args, **kwargs)
