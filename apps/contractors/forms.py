"""
Contractor forms for Event Management System.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Contractor, ContractorMember

CSS_INPUT = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
CSS_SELECT = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent bg-white'
CSS_TEXTAREA = CSS_INPUT
CSS_FILE = 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-black file:text-white hover:file:bg-gray-800'


class ContractorForm(forms.ModelForm):
    """Form for creating and updating contractors."""

    class Meta:
        model = Contractor
        fields = [
            'name', 'trade_name', 'cnpj', 'state_registration', 'legal_representative',
            'phone', 'email', 'website',
            'address_street', 'address_number', 'address_complement',
            'address_neighborhood', 'address_city', 'address_state', 'address_zip',
            'bank_name', 'bank_agency', 'bank_account', 'bank_account_type', 'bank_pix_key',
            'certifications', 'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Razão social da empreiteira'}),
            'trade_name': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Nome fantasia'}),
            'cnpj': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '00.000.000/0001-00'}),
            'state_registration': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Inscrição estadual'}),
            'legal_representative': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Nome do responsável legal'}),
            'phone': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': CSS_INPUT, 'placeholder': 'email@empresa.com'}),
            'website': forms.URLInput(attrs={'class': CSS_INPUT, 'placeholder': 'https://empresa.com.br'}),
            'address_street': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Rua / Avenida'}),
            'address_number': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Número'}),
            'address_complement': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Apto, Sala, etc.'}),
            'address_neighborhood': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Bairro'}),
            'address_city': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Cidade'}),
            'address_state': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'UF', 'maxlength': '2'}),
            'address_zip': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '00000-000'}),
            'bank_name': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Nome do banco'}),
            'bank_agency': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '0000-0'}),
            'bank_account': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '00000-0'}),
            'bank_account_type': forms.Select(attrs={'class': CSS_SELECT}),
            'bank_pix_key': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'CPF, CNPJ, e-mail, telefone ou chave aleatória'}),
            'certifications': forms.Textarea(attrs={'class': CSS_TEXTAREA, 'rows': 4, 'placeholder': 'Descreva certificações, alvarás e documentações'}),
            'notes': forms.Textarea(attrs={'class': CSS_TEXTAREA, 'rows': 3, 'placeholder': 'Observações gerais'}),
        }


class ContractorMemberForm(forms.ModelForm):
    """Form for individual contractor members – all sections."""

    class Meta:
        model = ContractorMember
        fields = [
            # Dados Pessoais
            'name', 'rg', 'cpf', 'birth_date', 'photo',
            # Dados Profissionais
            'role', 'specialty', 'experience_years',
            # NR
            'nr_number', 'nr_certificate_expiry', 'nr_certificate_file',
            # ASO
            'aso_number', 'aso_issue_date', 'aso_expiry_date', 'aso_exam_type', 'aso_file',
            # Contato
            'phone', 'emergency_phone', 'email',
            # Endereço
            'address_street', 'address_number', 'address_complement',
            'address_neighborhood', 'address_city', 'address_state', 'address_zip',
            # Observações
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Nome completo'}),
            'rg': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Ex: 12.345.678-9'}),
            'cpf': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '000.000.000-00'}),
            'birth_date': forms.DateInput(attrs={'class': CSS_INPUT, 'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': CSS_FILE}),
            'role': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Ex: Eletricista, Técnico de Som'}),
            'specialty': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Ex: Alta tensão, Áudio ao vivo'}),
            'experience_years': forms.NumberInput(attrs={'class': CSS_INPUT, 'placeholder': 'Anos', 'min': '0'}),
            'nr_number': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Ex: NR-10, NR-35, NR-33'}),
            'nr_certificate_expiry': forms.DateInput(attrs={'class': CSS_INPUT, 'type': 'date'}),
            'nr_certificate_file': forms.FileInput(attrs={'class': CSS_FILE}),
            'aso_number': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Número do ASO'}),
            'aso_issue_date': forms.DateInput(attrs={'class': CSS_INPUT, 'type': 'date'}),
            'aso_expiry_date': forms.DateInput(attrs={'class': CSS_INPUT, 'type': 'date'}),
            'aso_exam_type': forms.Select(attrs={'class': CSS_SELECT}),
            'aso_file': forms.FileInput(attrs={'class': CSS_FILE}),
            'phone': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '(00) 00000-0000'}),
            'emergency_phone': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': CSS_INPUT, 'placeholder': 'email@membro.com'}),
            'address_street': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Rua / Avenida'}),
            'address_number': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Número'}),
            'address_complement': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Apto, Sala, etc.'}),
            'address_neighborhood': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Bairro'}),
            'address_city': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'Cidade'}),
            'address_state': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': 'UF', 'maxlength': '2'}),
            'address_zip': forms.TextInput(attrs={'class': CSS_INPUT, 'placeholder': '00000-000'}),
            'notes': forms.Textarea(attrs={'class': CSS_TEXTAREA, 'rows': 3, 'placeholder': 'Observações sobre o profissional'}),
        }


# Inline formset used on Contractor create/edit (quick member addition)
ContractorMemberFormSet = inlineformset_factory(
    Contractor,
    ContractorMember,
    form=ContractorMemberForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False
)


class ContractorSearchForm(forms.Form):
    """Form for searching contractors."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar empreiteiras...'
        })
    )
