"""
Django admin registration for Logistics app.
"""

from django.contrib import admin
from .models import FreightSettings, UrgencyMultiplier, VolumeRange, WeightRange


@admin.register(FreightSettings)
class FreightSettingsAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'fixed_delivery_fee', 'percentage_on_total',
                    'calculation_mode', 'updated_at']
    readonly_fields = ['updated_at']

    def has_add_permission(self, request):
        # Only one instance allowed
        return not FreightSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WeightRange)
class WeightRangeAdmin(admin.ModelAdmin):
    list_display = ['label', 'min_weight', 'max_weight', 'rate', 'rate_type', 'order']
    list_editable = ['order']
    ordering = ['order', 'min_weight']


@admin.register(VolumeRange)
class VolumeRangeAdmin(admin.ModelAdmin):
    list_display = ['label', 'min_volume', 'max_volume', 'rate', 'rate_type', 'order']
    list_editable = ['order']
    ordering = ['order', 'min_volume']


@admin.register(UrgencyMultiplier)
class UrgencyMultiplierAdmin(admin.ModelAdmin):
    list_display = ['label', 'multiplier', 'description', 'is_default']
    list_editable = ['is_default']
