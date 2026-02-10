"""
Admin configuration for teams app.
"""

from django.contrib import admin
from .models import Team, TeamMember, EventTeam


class TeamMemberInline(admin.TabularInline):
    """Inline admin for team members."""
    model = TeamMember
    extra = 1
    fields = ('name', 'role', 'phone')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model."""
    
    list_display = ('name', 'member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    inlines = [TeamMemberInline]
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Membros'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    """Admin interface for TeamMember model."""
    
    list_display = ('name', 'role', 'team', 'phone', 'created_at')
    list_filter = ('role', 'team', 'created_at')
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
