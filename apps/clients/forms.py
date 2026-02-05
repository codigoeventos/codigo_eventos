"""
Client forms for Event Management System.
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button
from .models import Client
from apps.common.utils import validate_cpf, validate_cnpj


class ClientForm(forms.ModelForm):
    """Form for creating and updating Client instances."""
    
    class Meta:
        model = Client
        fields = ['name', 'document_type', 'document_number', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
                'placeholder': 'Nome completo ou razão social'
            }),
            'document_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all'
            }),
            'document_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
                'placeholder': 'CPF ou CNPJ'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
                'placeholder': 'email@exemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
                'placeholder': '(11) 99999-9999'
            }),
        }
    
    def clean_document_number(self):
        """Validate document number based on document type."""
        document_type = self.cleaned_data.get('document_type')
        document_number = self.cleaned_data.get('document_number')
        
        if not document_number:
            raise forms.ValidationError('Documento é obrigatório.')
        
        # Remove formatting
        document_number = ''.join(filter(str.isdigit, document_number))
        
        if document_type == 'CPF':
            if not validate_cpf(document_number):
                raise forms.ValidationError('CPF inválido.')
        elif document_type == 'CNPJ':
            if not validate_cnpj(document_number):
                raise forms.ValidationError('CNPJ inválido.')
        
        return document_number
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields
        for field_name, field in self.fields.items():
            if field.required:
                field.label = f"{field.label} *"


class ClientSearchForm(forms.Form):
    """Form for searching clients."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
            'placeholder': 'Buscar por nome, email ou documento...'
        })
    )
    
    document_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + Client.DOCUMENT_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all'
        })
    )
