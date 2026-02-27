"""
Forms for the Logistics / Freight configuration app.
"""

from django import forms
from .models import FreightSettings, UrgencyMultiplier, VolumeRange, WeightRange

_field_class = (
    'w-full px-4 py-2 border border-gray-300 rounded-lg '
    'focus:ring-2 focus:ring-black focus:border-transparent'
)
_checkbox_class = 'w-4 h-4 text-black border-gray-300 rounded focus:ring-black'


class FreightSettingsForm(forms.ModelForm):

    class Meta:
        model = FreightSettings
        fields = [
            'fixed_delivery_fee',
            'percentage_on_total',
            'calculation_mode',
            'distance_rate_enabled',
            'distance_rate_per_km',
        ]
        widgets = {
            'fixed_delivery_fee': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
            }),
            'percentage_on_total': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0', 'max': '100',
            }),
            'calculation_mode': forms.Select(attrs={'class': _field_class}),
            'distance_rate_enabled': forms.CheckboxInput(attrs={'class': _checkbox_class}),
            'distance_rate_per_km': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
            }),
        }


class WeightRangeForm(forms.ModelForm):

    class Meta:
        model = WeightRange
        fields = ['label', 'min_weight', 'max_weight', 'rate', 'rate_type', 'order']
        widgets = {
            'label': forms.TextInput(attrs={'class': _field_class, 'placeholder': 'Ex: Até 50 kg'}),
            'min_weight': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
            }),
            'max_weight': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
                'placeholder': 'Vazio = sem limite',
            }),
            'rate': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
            }),
            'rate_type': forms.Select(attrs={'class': _field_class}),
            'order': forms.NumberInput(attrs={'class': _field_class, 'min': '0'}),
        }
        labels = {
            'label': 'Descrição da Faixa',
            'min_weight': 'Peso Mínimo (kg)',
            'max_weight': 'Peso Máximo (kg)',
            'rate': 'Valor (R$)',
            'rate_type': 'Tipo de Cobrança',
            'order': 'Ordem de Exibição',
        }


class VolumeRangeForm(forms.ModelForm):

    class Meta:
        model = VolumeRange
        fields = ['label', 'min_volume', 'max_volume', 'rate', 'rate_type', 'order']
        widgets = {
            'label': forms.TextInput(attrs={'class': _field_class, 'placeholder': 'Ex: Até 1 m³'}),
            'min_volume': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.001', 'min': '0',
            }),
            'max_volume': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.001', 'min': '0',
                'placeholder': 'Vazio = sem limite',
            }),
            'rate': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0',
            }),
            'rate_type': forms.Select(attrs={'class': _field_class}),
            'order': forms.NumberInput(attrs={'class': _field_class, 'min': '0'}),
        }
        labels = {
            'label': 'Descrição da Faixa',
            'min_volume': 'Volume Mínimo (m³)',
            'max_volume': 'Volume Máximo (m³)',
            'rate': 'Valor (R$)',
            'rate_type': 'Tipo de Cobrança',
            'order': 'Ordem de Exibição',
        }


class UrgencyMultiplierForm(forms.ModelForm):

    class Meta:
        model = UrgencyMultiplier
        fields = ['label', 'description', 'multiplier', 'is_default']
        widgets = {
            'label': forms.TextInput(attrs={
                'class': _field_class, 'placeholder': 'Ex: Urgente',
            }),
            'description': forms.TextInput(attrs={
                'class': _field_class,
                'placeholder': 'Ex: Entrega em até 24h',
            }),
            'multiplier': forms.NumberInput(attrs={
                'class': _field_class, 'step': '0.01', 'min': '0.01',
            }),
            'is_default': forms.CheckboxInput(attrs={'class': _checkbox_class}),
        }
        labels = {
            'label': 'Nome',
            'description': 'Descrição',
            'multiplier': 'Multiplicador',
            'is_default': 'Padrão nos orçamentos',
        }
