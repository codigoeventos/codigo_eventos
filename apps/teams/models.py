"""
Team models for event staff management.
"""

from django.db import models


class TeamMember(models.Model):
    """
    Team member model representing staff that can be assigned to events.
    """
    
    name = models.CharField(
        'Nome',
        max_length=255
    )
    
    role = models.CharField(
        'Função',
        max_length=100,
        help_text='Ex: Técnico de Som, Iluminador, etc.'
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=50
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Membro da Equipe'
        verbose_name_plural = 'Membros da Equipe'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class EventTeam(models.Model):
    """
    Association between events and team members.
    """
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='team_assignments',
        verbose_name='Evento'
    )
    
    member = models.ForeignKey(
        'TeamMember',
        on_delete=models.CASCADE,
        related_name='event_assignments',
        verbose_name='Membro'
    )
    
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Equipe do Evento'
        verbose_name_plural = 'Equipes dos Eventos'
        unique_together = [['event', 'member']]
        ordering = ['event', 'member']
    
    def __str__(self):
        return f"{self.event} - {self.member}"
