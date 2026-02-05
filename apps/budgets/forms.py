"""
Budget forms for Event Management System.
"""

from django import forms
from .models import Budget


class BudgetForm(forms.ModelForm):
    """Form for creating and updating budgets."""
    
    class Meta:
        model = Budget
        fields = ['proposal', 'name', 'status', 'is_selected']
        widgets = {
            'proposal': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome do orçamento'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'is_selected': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-black focus:ring-black border-gray-300 rounded'
            }),
        }
        labels = {
            'proposal': 'Proposta',
            'name': 'Nome',
            'status': 'Status',
            'is_selected': 'Selecionado',
        }


class BudgetSearchForm(forms.Form):
    """Form for searching budgets."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar orçamentos...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + Budget.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
        })
    )
    
    proposal = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todas as propostas',
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.proposals.models import Proposal
        self.fields['proposal'].queryset = Proposal.objects.all().order_by('-created_at')
