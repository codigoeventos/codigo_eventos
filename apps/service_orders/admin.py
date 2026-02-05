"""
Admin configuration for service orders app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ServiceOrder, ServiceOrderItem


class ServiceOrderItemInline(admin.TabularInline):
    """Inline admin for service order items."""
    
    model = ServiceOrderItem
    extra = 1
    fields = ('name', 'description', 'quantity', 'execution_status')


@admin.register(ServiceOrder)
class ServiceOrderAdmin(SimpleHistoryAdmin):
    """Admin interface for ServiceOrder model."""
    
    list_display = ('id', 'event', 'budget', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('event__name', 'budget__name')
    ordering = ('-created_at',)
    inlines = [ServiceOrderItemInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('event', 'budget')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')


@admin.register(ServiceOrderItem)
class ServiceOrderItemAdmin(admin.ModelAdmin):
    """Admin interface for ServiceOrderItem model."""
    
    list_display = ('name', 'service_order', 'quantity', 'execution_status')
    list_filter = ('execution_status',)
    search_fields = ('name', 'description')
