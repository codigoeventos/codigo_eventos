"""
Admin configuration for events app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Event


@admin.register(Event)
class EventAdmin(SimpleHistoryAdmin):
    """Admin interface for Event model."""
    
    list_display = ('name', 'client', 'event_date', 'location', 'created_at')
    list_filter = ('event_date', 'created_at')
    search_fields = ('name', 'location', 'client__name')
    ordering = ('-event_date',)
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Informações do Evento', {
            'fields': ('client', 'name', 'event_date', 'location')
        }),
        ('Detalhes', {
            'fields': ('notes',)
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
