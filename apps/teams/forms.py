"""
Team forms for Event Management System.
"""

from django import forms
from .models import TeamMember


class TeamMemberForm(forms.ModelForm):
    """Form for creating and updating team members."""
    
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome completo'
            }),
            'role': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Ex: Técnico de Som, Iluminador, etc.'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': '(00) 00000-0000'
            }),
        }
        labels = {
            'name': 'Nome',
            'role': 'Função',
            'phone': 'Telefone',
        }


class TeamMemberSearchForm(forms.Form):
    """Form for searching team members."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar membros...'
        })
    )
