"""
ART forms.
"""

from django import forms
from .models import ART

_cls = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
_cls_sm = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent text-sm'


class ARTEditForm(forms.ModelForm):
    """
    Form for editing an ART after auto-generation.
    Allows filling in engineer data and adjusting auto-populated fields.
    """

    class Meta:
        model = ART
        fields = [
            # Engenheiro
            'engineer_name', 'engineer_crea',
            # Contratante – nome e documento
            'contratante_nome', 'contratante_cnpj',
            # Contratado
            'client_address', 'client_number', 'client_complement',
            'client_neighborhood', 'client_city', 'client_state', 'client_zip',
            'tipo_contratante',
            # Obra
            'obra_address', 'obra_number', 'obra_complement',
            'obra_neighborhood', 'obra_city', 'obra_state', 'obra_zip',
            'start_date', 'end_date',
            # Atividades
            'nivel_atuacao', 'atividade', 'atividade_complemento', 'obra_servico',
            'quantity', 'measurement_unit',
            # Contrato / financeiro
            'contract_value',
            # Observações / legado
            'activity_description', 'notes',
        ]
        widgets = {
            'engineer_name': forms.TextInput(attrs={'class': _cls, 'placeholder': 'Nome completo do engenheiro responsável'}),
            'engineer_crea': forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex: CREA-SP 1234567/D'}),
            # Contratante – nome e documento
            'contratante_nome': forms.TextInput(attrs={'class': _cls, 'placeholder': 'Nome ou razão social do contratante'}),
            'contratante_cnpj': forms.TextInput(attrs={'class': _cls, 'placeholder': '00.000.000/0000-00'}),
            # Contratado
            'client_address':      forms.TextInput(attrs={'class': _cls, 'placeholder': 'Rua / Avenida'}),
            'client_number':       forms.TextInput(attrs={'class': _cls, 'placeholder': 'N°'}),
            'client_complement':   forms.TextInput(attrs={'class': _cls, 'placeholder': '2º pav, Apto 3...'}),
            'client_neighborhood': forms.TextInput(attrs={'class': _cls, 'placeholder': 'Bairro'}),
            'client_city':         forms.TextInput(attrs={'class': _cls, 'placeholder': 'Cidade'}),
            'client_state':        forms.TextInput(attrs={'class': _cls, 'placeholder': 'UF', 'maxlength': 2}),
            'client_zip':          forms.TextInput(attrs={'class': _cls, 'placeholder': '00000-000'}),
            'tipo_contratante':    forms.Select(attrs={'class': _cls}),
            # Obra
            'obra_address':        forms.TextInput(attrs={'class': _cls, 'placeholder': 'Rua / Avenida'}),
            'obra_number':         forms.TextInput(attrs={'class': _cls, 'placeholder': 'N°'}),
            'obra_complement':     forms.TextInput(attrs={'class': _cls, 'placeholder': 'Pavilhão, Bloco...'}),
            'obra_neighborhood':   forms.TextInput(attrs={'class': _cls, 'placeholder': 'Bairro'}),
            'obra_city':           forms.TextInput(attrs={'class': _cls, 'placeholder': 'Cidade'}),
            'obra_state':          forms.TextInput(attrs={'class': _cls, 'placeholder': 'UF', 'maxlength': 2}),
            'obra_zip':            forms.TextInput(attrs={'class': _cls, 'placeholder': '00000-000'}),
            'start_date':          forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            'end_date':            forms.DateInput(attrs={'class': _cls, 'type': 'date'}),
            # Atividades
            'nivel_atuacao':          forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex: FISCALIZAÇÃO'}),
            'atividade':              forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex: MONTAGEM'}),
            'atividade_complemento':  forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex: INSTALAÇÃO PROVISÓRIA'}),
            'obra_servico':           forms.TextInput(attrs={'class': _cls, 'placeholder': 'Ex: EDIFICAÇÃO DE MATERIAIS MISTOS'}),
            'quantity':               forms.NumberInput(attrs={'class': _cls, 'step': '0.001', 'min': '0'}),
            'measurement_unit':       forms.Select(attrs={'class': _cls}),
            # Contrato
            'contract_value': forms.NumberInput(attrs={'class': _cls, 'step': '0.01', 'min': '0', 'placeholder': '0,00'}),
            # Legado
            'activity_description': forms.Textarea(attrs={'class': _cls, 'rows': 4, 'placeholder': 'Observação / Descrição adicional'}),
            'notes': forms.Textarea(attrs={'class': _cls, 'rows': 3, 'placeholder': 'Observações adicionais (opcional)'}),
        }
        labels = {
            'engineer_name': 'Nome do Engenheiro',
            'engineer_crea': 'CREA',
            'contratante_nome': 'Nome do Contratante',
            'contratante_cnpj': 'CNPJ do Contratante',
            'client_address': 'Endereço', 'client_number': 'N°', 'client_complement': 'Complemento',
            'client_neighborhood': 'Bairro', 'client_city': 'Cidade', 'client_state': 'UF', 'client_zip': 'CEP',
            'tipo_contratante': 'Tipo de Contratante',
            'obra_address': 'Endereço', 'obra_number': 'N°', 'obra_complement': 'Complemento',
            'obra_neighborhood': 'Bairro', 'obra_city': 'Cidade', 'obra_state': 'UF', 'obra_zip': 'CEP',
            'start_date': 'Data de Início', 'end_date': 'Data de Término',
            'nivel_atuacao': 'Nível de Atuação', 'atividade': 'Atividade',
            'atividade_complemento': 'Complemento', 'obra_servico': 'Obra / Serviço',
            'quantity': 'Quantidade Total', 'measurement_unit': 'Unidade de Medida',
            'contract_value': 'Valor do Contrato (R$)',
            'activity_description': 'Observação do Documento',
            'notes': 'Observações',
        }
        help_texts = {
            'quantity': 'Calculado automaticamente como soma da metragem dos itens do orçamento',
        }