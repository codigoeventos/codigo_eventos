"""
ART forms.
"""

from django import forms
from .models import ART

_cls = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'


class ARTEditForm(forms.ModelForm):
    """
    Form for editing all information printed in an ART.

    The event/OS is used only to pre-fill this form when the ART is created;
    once saved, the ART fields themselves are the source of truth.
    """

    class Meta:
        model = ART
        fields = [
            'engineer_name', 'engineer_crea',
            'contratante_nome', 'contratante_cnpj',
            'client_address', 'client_number', 'client_complement',
            'client_neighborhood', 'client_city', 'client_state', 'client_zip',
            'tipo_contratante',
            'obra_address', 'obra_number', 'obra_complement',
            'obra_neighborhood', 'obra_city', 'obra_state', 'obra_zip',
            'nivel_atuacao', 'atividade', 'atividade_complemento', 'obra_servico',
            'activity_description', 'location',
            'quantity', 'measurement_unit',
            'start_date', 'end_date',
            'notes',
        ]
        widgets = {
            'engineer_name':       forms.TextInput(attrs={'class': _cls, 'placeholder': 'Nome completo'}),
            'engineer_crea':       forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex.: CREA-SP 123456/D'}),
            'contratante_nome':    forms.TextInput(attrs={'class': _cls, 'placeholder': 'Nome ou razão social'}),
            'contratante_cnpj':    forms.TextInput(attrs={'class': _cls, 'placeholder': 'CPF ou CNPJ'}),
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
            'nivel_atuacao':       forms.TextInput(attrs={'class': _cls}),
            'atividade':           forms.TextInput(attrs={'class': _cls}),
            'atividade_complemento': forms.TextInput(attrs={'class': _cls}),
            'obra_servico':        forms.TextInput(attrs={'class': _cls}),
            'activity_description': forms.Textarea(attrs={'class': _cls, 'rows': 3}),
            'location':            forms.TextInput(attrs={'class': _cls, 'placeholder': 'Referência do local da obra'}),
            'quantity':            forms.NumberInput(attrs={'class': _cls, 'step': '0.001', 'min': '0'}),
            'measurement_unit':    forms.Select(attrs={'class': _cls}),
            'start_date':          forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            'end_date':            forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            'notes':               forms.Textarea(attrs={'class': _cls, 'rows': 2, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'engineer_name': 'Nome do Engenheiro', 'engineer_crea': 'CREA do Engenheiro',
            'contratante_nome': 'Contratante', 'contratante_cnpj': 'CPF/CNPJ do Contratante',
            'client_address': 'Endereço', 'client_number': 'N°', 'client_complement': 'Complemento',
            'client_neighborhood': 'Bairro', 'client_city': 'Cidade', 'client_state': 'UF', 'client_zip': 'CEP',
            'tipo_contratante': 'Tipo de Contratante',
            'obra_address': 'Endereço', 'obra_number': 'N°', 'obra_complement': 'Complemento',
            'obra_neighborhood': 'Bairro', 'obra_city': 'Cidade', 'obra_state': 'UF', 'obra_zip': 'CEP',
            'nivel_atuacao': 'Nível de Atuação', 'atividade': 'Atividade',
            'atividade_complemento': 'Complemento da Atividade', 'obra_servico': 'Obra / Serviço',
            'activity_description': 'Descrição da Atividade / Serviço', 'location': 'Local da Obra (referência)',
            'quantity': 'Quantidade', 'measurement_unit': 'Unidade',
            'start_date': 'Data Início', 'end_date': 'Data Conclusão',
            'notes': 'Observações',
        }
        help_texts = {
            'quantity': 'Calculado automaticamente como soma da metragem dos itens do orçamento',
        }
