"""
ART forms.
"""

from django import forms
from .models import ART

_cls = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'


class ARTEditForm(forms.ModelForm):
    """
    Form for editing an ART after auto-generation.
    Must mirror exactly the fields shown in the generate modal.
    """

    class Meta:
        model = ART
        fields = [
            'client_address', 'client_number', 'client_complement',
            'client_neighborhood', 'client_city', 'client_state', 'client_zip',
            'tipo_contratante',
            'obra_address', 'obra_number', 'obra_complement',
            'obra_neighborhood', 'obra_city', 'obra_state', 'obra_zip',
            'quantity', 'measurement_unit',
            'start_date', 'end_date',
            'notes',
        ]
        widgets = {
            'client_address':      forms.TextInput(attrs={'class': _cls, 'placeholder': 'Rua / Avenida'}),
            'client_number':       forms.TextInput(attrs={'class': _cls, 'placeholder': 'N°'}),
            'client_complement':   forms.TextInput(attrs={'class': _cls, 'placeholder': '2º pav, Apto 3...'}),
            'client_neighborhood': forms.TextInput(attrs={'class': _cls, 'placeholder': 'Bairro'}),
            'client_city':         forms.TextInput(attrs={'class': _cls, 'placeholder': 'Cidade'}),
            'client_state':        forms.TextInput(attrs={'class': _cls, 'placeholder': 'UF', 'maxlength': 2}),
            'client_zip':          forms.TextInput(attrs={'class': _cls, 'placeholder': '00000-000'}),
            'tipo_contratante':    forms.Select(attrs={'class': _cls}),
            'obra_address':        forms.TextInput(attrs={'class': _cls, 'placeholder': 'Rua / Avenida'}),
            'obra_number':         forms.TextInput(attrs={'class': _cls, 'placeholder': 'N°'}),
            'obra_complement':     forms.TextInput(attrs={'class': _cls, 'placeholder': 'Pavilhão, Bloco...'}),
            'obra_neighborhood':   forms.TextInput(attrs={'class': _cls, 'placeholder': 'Bairro'}),
            'obra_city':           forms.TextInput(attrs={'class': _cls, 'placeholder': 'Cidade'}),
            'obra_state':          forms.TextInput(attrs={'class': _cls, 'placeholder': 'UF', 'maxlength': 2}),
            'obra_zip':            forms.TextInput(attrs={'class': _cls, 'placeholder': '00000-000'}),
            'quantity':            forms.NumberInput(attrs={'class': _cls, 'step': '0.001', 'min': '0'}),
            'measurement_unit':    forms.Select(attrs={'class': _cls}),
            'start_date':          forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            'end_date':            forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            'notes':               forms.Textarea(attrs={'class': _cls, 'rows': 2, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'client_address': 'Endereço', 'client_number': 'N°', 'client_complement': 'Complemento',
            'client_neighborhood': 'Bairro', 'client_city': 'Cidade', 'client_state': 'UF', 'client_zip': 'CEP',
            'tipo_contratante': 'Tipo de Contratante',
            'obra_address': 'Endereço', 'obra_number': 'N°', 'obra_complement': 'Complemento',
            'obra_neighborhood': 'Bairro', 'obra_city': 'Cidade', 'obra_state': 'UF', 'obra_zip': 'CEP',
            'quantity': 'Quantidade', 'measurement_unit': 'Unidade',
            'start_date': 'Data Início', 'end_date': 'Data Conclusão',
            'notes': 'Observações',
        }
        help_texts = {
            'quantity': 'Calculado automaticamente como soma da metragem dos itens do orçamento',
        }
