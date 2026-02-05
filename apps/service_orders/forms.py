"""
Service Order forms for Event Management System.
"""

from django import forms
from .models import ServiceOrder


class ServiceOrderForm(forms.ModelForm):
    """Form for creating and updating service orders."""
    
    class Meta:
        model = ServiceOrder
        fields = ['budget', 'event', 'status']
        widgets = {
            'budget': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'event': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
        }
        labels = {
            'budget': 'Orçamento',
            'event': 'Evento',
            'status': 'Status',
        }


class ServiceOrderSearchForm(forms.Form):
    """Form for searching service orders."""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar ordens de serviço...'
        })
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + ServiceOrder.STATUS_CHOICES,
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
