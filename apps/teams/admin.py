"""
Admin configuration for teams app.
"""

from django.contrib import admin
from .models import TeamMember, EventTeam


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for TeamMember model."""
    
    list_display = ('name', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'role')
    ordering = ('name',)


@admin.register(EventTeam)
class EventTeamAdmin(admin.ModelAdmin):
    """Admin interface for EventTeam model."""
    
    list_display = ('event', 'member', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('event__name', 'member__name')
    ordering = ('-assigned_at',)
    autocomplete_fields = ['event', 'member']
