"""
Admin configuration for budgets app.
"""

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Budget, BudgetItem, BudgetSection, ItemDescription


class BudgetSectionInline(admin.TabularInline):
    """Inline admin for budget sections."""
    model = BudgetSection
    extra = 0
    fields = ('title', 'order')


class BudgetItemInline(admin.TabularInline):
    """Inline admin for budget items."""
    
    model = BudgetItem
    extra = 1
    fields = ('section', 'name', 'description', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Budget)
class BudgetAdmin(SimpleHistoryAdmin):
    """Admin interface for Budget model."""
    
    list_display = ('name', 'proposal', 'status', 'is_selected', 'total_value', 'created_at')
    list_filter = ('status', 'is_selected', 'created_at')
    search_fields = ('name', 'proposal__title')
    ordering = ('-created_at',)
    inlines = [BudgetSectionInline, BudgetItemInline]
    
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
    
    list_display = ('name', 'budget', 'section', 'quantity', 'unit_price', 'total_price')
    list_filter = ('budget', 'section')
    search_fields = ('name', 'description')
    readonly_fields = ('total_price',)


@admin.register(BudgetSection)
class BudgetSectionAdmin(admin.ModelAdmin):
    """Admin interface for BudgetSection model."""

    list_display = ('title', 'budget', 'order', 'subtotal')
    list_filter = ('budget',)
    search_fields = ('title', 'budget__name')
    ordering = ('budget', 'order')


@admin.register(ItemDescription)
class ItemDescriptionAdmin(admin.ModelAdmin):
    """Admin interface for the item description library."""

    list_display  = ('title', 'body_preview', 'created_at')
    search_fields = ('title', 'body')
    ordering      = ('title',)

    @admin.display(description='Descrição (prévia)')
    def body_preview(self, obj):
        return obj.body[:80] + '…' if len(obj.body) > 80 else obj.body

