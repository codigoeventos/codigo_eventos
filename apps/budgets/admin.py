"""
Admin configuration for budgets app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Budget, BudgetItem


class BudgetItemInline(admin.TabularInline):
    """Inline admin for budget items."""
    
    model = BudgetItem
    extra = 1
    fields = ('name', 'description', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Budget)
class BudgetAdmin(SimpleHistoryAdmin):
    """Admin interface for Budget model."""
    
    list_display = ('name', 'proposal', 'status', 'is_selected', 'total_value', 'created_at')
    list_filter = ('status', 'is_selected', 'created_at')
    search_fields = ('name', 'proposal__title')
    ordering = ('-created_at',)
    inlines = [BudgetItemInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('proposal', 'name')
        }),
        ('Status', {
            'fields': ('status', 'is_selected')
        }),
        ('Auditoria', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')


@admin.register(BudgetItem)
class BudgetItemAdmin(admin.ModelAdmin):
    """Admin interface for BudgetItem model."""
    
    list_display = ('name', 'budget', 'quantity', 'unit_price', 'total_price')
    list_filter = ('budget',)
    search_fields = ('name', 'description')
    readonly_fields = ('total_price',)
