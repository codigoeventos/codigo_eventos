"""
ART forms.
"""

from django import forms
from .models import ART


class ARTEditForm(forms.ModelForm):
    """
    Form for editing an ART after auto-generation.
    Allows filling in engineer data and adjusting auto-populated fields.
    """

    class Meta:
        model = ART
        fields = [
            'engineer_name',
            'engineer_crea',
            'activity_description',
            'location',
            'quantity',
            'measurement_unit',
            'contract_value',
            'start_date',
            'end_date',
            'notes',
        ]
        widgets = {
            'engineer_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome completo do engenheiro responsável',
            }),
            'engineer_crea': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Ex: CREA-SP 1234567/D',
            }),
            'activity_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'rows': 4,
                'placeholder': 'Descreva as atividades técnicas a serem executadas',
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Endereço completo da obra / evento',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.001',
                'min': '0',
            }),
            'measurement_unit': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            }),
            'contract_value': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00',
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'type': 'date',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'rows': 3,
                'placeholder': 'Observações adicionais (opcional)',
            }),
        }
        labels = {
            'engineer_name': 'Nome do Engenheiro',
            'engineer_crea': 'CREA',
            'activity_description': 'Descrição da Atividade / Serviço',
            'location': 'Local da Obra / Endereço',
            'quantity': 'Quantidade Total',
            'measurement_unit': 'Unidade de Medida',
            'contract_value': 'Valor do Contrato (R$)',
            'start_date': 'Data de Início',
            'end_date': 'Data de Conclusão',
            'notes': 'Observações',
        }
        help_texts = {
            'quantity': 'Calculado automaticamente como soma da metragem dos itens do orçamento',
        }
