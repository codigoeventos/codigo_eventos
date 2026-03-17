from django.contrib import admin
from .models import ART


@admin.register(ART)
class ARTAdmin(admin.ModelAdmin):
    list_display = ['art_number', 'project', 'engineer_name', 'engineer_crea', 'created_at']
    list_filter = ['created_at']
    search_fields = ['project__title', 'engineer_name', 'engineer_crea']
    readonly_fields = ['public_token', 'created_at', 'updated_at', 'created_by', 'updated_by']
