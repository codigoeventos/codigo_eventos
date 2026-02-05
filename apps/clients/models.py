"""
Client model for the Event Management System.
"""

from django.db import models
from django.core.exceptions import ValidationError
from apps.common.models import BaseModel
from apps.common.utils import validate_cpf, validate_cnpj, format_cpf, format_cnpj


class Client(BaseModel):
    """
    Client model representing customers who hire events.
    
    Can be either a natural person (CPF) or legal entity (CNPJ).
    """
    
    DOCUMENT_TYPE_CHOICES = [
        ('cpf', 'CPF'),
        ('cnpj', 'CNPJ'),
    ]
    
    name = models.CharField(
        'Nome',
        max_length=255,
        help_text='Nome completo ou razão social'
    )
    
    document_type = models.CharField(
        'Tipo de Documento',
        max_length=4,
        choices=DOCUMENT_TYPE_CHOICES
    )
    
    document_number = models.CharField(
        'Número do Documento',
        max_length=18,
        help_text='CPF ou CNPJ'
    )
    
    email = models.EmailField(
        'E-mail',
        blank=True,
        null=True
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=20
    )
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def clean(self):
        """Validate document number based on document type."""
        super().clean()
        
        if self.document_type == 'cpf':
            if not validate_cpf(self.document_number):
                raise ValidationError({'document_number': 'CPF inválido.'})
            self.document_number = format_cpf(self.document_number)
        
        elif self.document_type == 'cnpj':
            if not validate_cnpj(self.document_number):
                raise ValidationError({'document_number': 'CNPJ inválido.'})
            self.document_number = format_cnpj(self.document_number)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
