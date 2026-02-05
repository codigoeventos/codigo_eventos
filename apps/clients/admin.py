"""
Admin configuration for clients app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Client


@admin.register(Client)
class ClientAdmin(SimpleHistoryAdmin):
    """Admin interface for Client model."""
    
    list_display = ('name', 'document_type', 'document_number', 'email', 'phone', 'created_at')
    list_filter = ('document_type', 'created_at')
    search_fields = ('name', 'document_number', 'email')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'document_type', 'document_number')
        }),
        ('Contato', {
            'fields': ('email', 'phone')
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
