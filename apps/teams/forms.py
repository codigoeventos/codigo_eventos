"""
Team forms for Event Management System.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Team, TeamMember


class TeamForm(forms.ModelForm):
    """Form for creating and updating teams."""
    
    class Meta:
        model = Team
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome da equipe'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Descrição das responsabilidades da equipe',
                'rows': 3
            }),
        }
        labels = {
            'name': 'Nome da Equipe',
            'description': 'Descrição',
        }


class TeamMemberForm(forms.ModelForm):
    """Form for individual team members within a team."""
    
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


# Formset for TeamMember
TeamMemberFormSet = inlineformset_factory(
    Team,
    TeamMember,
    form=TeamMemberForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False
)


class TeamSearchForm(forms.Form):
    """Form for searching teams."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar equipes...'
        })
    )
