"""
Admin configuration for technical visits app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import TechnicalVisit, TechnicalVisitAttachment


class TechnicalVisitAttachmentInline(admin.TabularInline):
    """Inline admin for visit attachments."""
    
    model = TechnicalVisitAttachment
    extra = 1
    fields = ('file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(TechnicalVisit)
class TechnicalVisitAdmin(SimpleHistoryAdmin):
    """Admin interface for TechnicalVisit model."""
    
    list_display = ('event', 'visit_date', 'responsible', 'status', 'created_at')
    list_filter = ('status', 'visit_date', 'created_at')
    search_fields = ('event__name', 'notes')
    ordering = ('-visit_date',)
    date_hierarchy = 'visit_date'
    inlines = [TechnicalVisitAttachmentInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('event', 'responsible', 'visit_date')
        }),
        ('Detalhes', {
            'fields': ('notes', 'status')
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')


@admin.register(TechnicalVisitAttachment)
class TechnicalVisitAttachmentAdmin(admin.ModelAdmin):
    """Admin interface for TechnicalVisitAttachment model."""
    
    list_display = ('visit', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('visit__event__name',)
    readonly_fields = ('uploaded_at',)
