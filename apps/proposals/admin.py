"""
Admin configuration for proposals app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Proposal


@admin.register(Proposal)
class ProposalAdmin(SimpleHistoryAdmin):
    """Admin interface for Proposal model."""
    
    list_display = ('title', 'event', 'status', 'total_value', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'event__name', 'description')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('event', 'title', 'description')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Documento', {
            'fields': ('original_document',)
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
