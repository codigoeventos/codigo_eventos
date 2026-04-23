"""
Event forms for Event Management System.
"""

from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """Form for creating and updating events."""
    
    class Meta:
        model = Event
        fields = ['client', 'name', 'setup_date', 'setup_date_end', 'event_date', 'event_date_end', 'teardown_date', 'teardown_date_end', 'location', 'notes']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome do evento'
            }),
            'setup_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'setup_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'event_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'event_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'teardown_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'teardown_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'}
            ),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Local do evento'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Observações adicionais'
            }),
        }
        labels = {
            'client': 'Cliente',
            'name': 'Nome do Evento',
            'setup_date': 'Início da Montagem',
            'setup_date_end': 'Término da Montagem',
            'event_date': 'Início do Evento',
            'event_date_end': 'Término do Evento',
            'teardown_date': 'Início da Desmontagem',
            'teardown_date_end': 'Término da Desmontagem',
            'location': 'Local',
            'notes': 'Observações',
        }


class EventSearchForm(forms.Form):
    """Form for searching events."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar eventos...'
        })
    )
    
    client = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todos os clientes',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.clients.models import Client
        self.fields['client'].queryset = Client.objects.all().order_by('name')
