"""
Proposal forms for Event Management System.
"""

from django import forms
from .models import Proposal


class ProposalForm(forms.ModelForm):
    """Form for creating and updating proposals."""
    
    class Meta:
        model = Proposal
        fields = ['event', 'title', 'description', 'status', 'original_document']
        widgets = {
            'event': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Título da proposta'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Descrição detalhada da proposta'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'original_document': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
        }
        labels = {
            'event': 'Evento',
            'title': 'Título',
            'description': 'Descrição',
            'status': 'Status',
            'original_document': 'Documento Original',
        }


class ProposalSearchForm(forms.Form):
    """Form for searching proposals."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar propostas...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + Proposal.STATUS_CHOICES,
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
        })
    )
    
    event = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todos os eventos',
        widget=forms.Select(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.events.models import Event
        self.fields['event'].queryset = Event.objects.all().order_by('-event_date')
