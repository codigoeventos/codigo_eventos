"""
Admin configuration for documents app.
"""

from django.contrib import admin
from .models import EventDocument


@admin.register(EventDocument)
class EventDocumentAdmin(admin.ModelAdmin):
    """Admin interface for EventDocument model."""
    
    list_display = ('event', 'doc_type', 'description', 'uploaded_at')
    list_filter = ('doc_type', 'uploaded_at')
    search_fields = ('event__name', 'description')
    ordering = ('-uploaded_at',)
    
    fieldsets = (
        ('Informações do Documento', {
            'fields': ('event', 'doc_type', 'description', 'file')
        }),
        ('Metadados', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('uploaded_at',)
