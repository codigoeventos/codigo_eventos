"""Core app models."""

from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Base model with common fields."""
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        abstract = True


class ExampleModel(BaseModel):
    """Modelo de exemplo."""
    
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descrição')
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='examples',
        verbose_name='Proprietário'
    )

    class Meta:
        verbose_name = 'Exemplo'
        verbose_name_plural = 'Exemplos'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
