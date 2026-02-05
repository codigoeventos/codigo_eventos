"""
Technical Visit forms for Event Management System.
"""

from django import forms
from .models import TechnicalVisit


class TechnicalVisitForm(forms.ModelForm):
    """Form for creating and updating technical visits."""
    
    class Meta:
        model = TechnicalVisit
        fields = ['event', 'responsible', 'visit_date', 'notes', 'status']
        widgets = {
            'event': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'responsible': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'visit_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Observações da visita técnica'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
        }
        labels = {
            'event': 'Evento',
            'responsible': 'Responsável',
            'visit_date': 'Data da Visita',
            'notes': 'Observações',
            'status': 'Status',
        }


class TechnicalVisitSearchForm(forms.Form):
    """Form for searching technical visits."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar visitas técnicas...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + TechnicalVisit.STATUS_CHOICES,
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
