"""
Admin configuration for contractors app.
"""

from django.contrib import admin
from .models import Contractor, ContractorMember, EventContractor


class ContractorMemberInline(admin.TabularInline):
    """Inline admin for contractor members."""
    model = ContractorMember
    extra = 1
    fields = ('name', 'role', 'cpf', 'phone', 'email')


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    """Admin interface for Contractor model."""

    list_display = ('name', 'trade_name', 'cnpj', 'legal_representative', 'phone', 'member_count', 'created_at')
    list_filter = ('created_at', 'address_state')
    search_fields = ('name', 'trade_name', 'cnpj', 'legal_representative', 'email')
    ordering = ('name',)
    inlines = [ContractorMemberInline]

    fieldsets = (
        ('Identificação', {
            'fields': ('name', 'trade_name', 'cnpj', 'state_registration', 'legal_representative', 'notes')
        }),
        ('Contato', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Endereço', {
            'fields': (
                'address_street', 'address_number', 'address_complement',
                'address_neighborhood', 'address_city', 'address_state', 'address_zip'
            )
        }),
        ('Dados Bancários', {
            'fields': ('bank_name', 'bank_agency', 'bank_account', 'bank_account_type', 'bank_pix_key'),
            'classes': ('collapse',)
        }),
        ('Documentação', {
            'fields': ('certifications',),
            'classes': ('collapse',)
        }),
    )

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Membros'


@admin.register(ContractorMember)
class ContractorMemberAdmin(admin.ModelAdmin):
    """Admin interface for ContractorMember model."""

    list_display = ('name', 'role', 'contractor', 'cpf', 'phone', 'aso_expiry_date', 'nr_certificate_expiry', 'created_at')
    list_filter = ('role', 'contractor', 'aso_exam_type', 'created_at')
    search_fields = ('name', 'cpf', 'rg', 'role')
    ordering = ('name',)

    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('contractor', 'name', 'rg', 'cpf', 'birth_date', 'photo')
        }),
        ('Dados Profissionais', {
            'fields': ('role', 'specialty', 'experience_years')
        }),
        ('NR – Norma Regulamentadora', {
            'fields': ('nr_number', 'nr_certificate_expiry', 'nr_certificate_file'),
            'classes': ('collapse',)
        }),
        ('ASO – Atestado de Saúde Ocupacional', {
            'fields': ('aso_number', 'aso_issue_date', 'aso_expiry_date', 'aso_exam_type', 'aso_file'),
            'classes': ('collapse',)
        }),
        ('Contato', {
            'fields': ('phone', 'emergency_phone', 'email')
        }),
        ('Endereço', {
            'fields': (
                'address_street', 'address_number', 'address_complement',
                'address_neighborhood', 'address_city', 'address_state', 'address_zip'
            ),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
    )


@admin.register(EventContractor)
class EventContractorAdmin(admin.ModelAdmin):
    """Admin interface for EventContractor model."""

    list_display = ('event', 'contractor', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('event__name', 'contractor__name')
    ordering = ('-assigned_at',)
    autocomplete_fields = ['event', 'contractor']
