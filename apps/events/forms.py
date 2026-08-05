"""
Event forms for Event Management System.
"""

from django import forms
from .models import Event

_INPUT_CLS = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'


class EventForm(forms.ModelForm):
    """Form for creating and updating events."""

    class Meta:
        model = Event
        fields = [
            'client', 'name',
            'setup_date', 'setup_date_end',
            'event_date', 'event_date_end',
            'teardown_date', 'teardown_date_end',
            'address', 'address_number', 'address_complement',
            'address_neighborhood', 'address_city', 'address_state', 'address_zip',
            'notes',
        ]
        widgets = {
            'client': forms.Select(attrs={'class': _INPUT_CLS}),
            'name': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'Nome do evento',
            }),
            'setup_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'setup_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'event_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'event_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'teardown_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'teardown_date_end': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'class': _INPUT_CLS},
            ),
            'address': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'Rua / Avenida',
            }),
            'address_number': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'Nº',
            }),
            'address_complement': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': '2º pav, Apto 3...',
            }),
            'address_neighborhood': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'Bairro',
            }),
            'address_city': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'Cidade',
            }),
            'address_state': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': 'UF',
                'maxlength': '2',
            }),
            'address_zip': forms.TextInput(attrs={
                'class': _INPUT_CLS,
                'placeholder': '00000-000',
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': _INPUT_CLS,
                'placeholder': 'Observações adicionais',
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
            'address': 'Endereço',
            'address_number': 'Nº',
            'address_complement': 'Complemento',
            'address_neighborhood': 'Bairro',
            'address_city': 'Cidade',
            'address_state': 'UF',
            'address_zip': 'CEP',
            'notes': 'Observações',
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        formatted = instance.format_full_address()
        if formatted:
            instance.location = formatted
        obj = instance
        if commit:
            obj.save()
            self.save_m2m()
        return obj


class EventSearchForm(forms.Form):
    """Form for searching events."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar eventos...',
        }),
    )

    client = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label='Todos os clientes',
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.clients.models import Client
        self.fields['client'].queryset = Client.objects.all().order_by('name')
