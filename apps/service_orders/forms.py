"""
Service Order forms for Event Management System.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import ServiceOrder, ServiceOrderItem


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


class ServiceOrderItemForm(forms.ModelForm):
    """Form for individual service order items."""
    
    class Meta:
        model = ServiceOrderItem
        fields = ['name', 'description', 'quantity', 'execution_status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome do item'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Descrição detalhada',
                'rows': 3
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'min': '1'
            }),
            'execution_status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
        }
        labels = {
            'name': 'Item',
            'description': 'Descrição',
            'quantity': 'Quantidade',
            'execution_status': 'Status de Execução',
        }


# Formset for ServiceOrderItem
ServiceOrderItemFormSet = inlineformset_factory(
    ServiceOrder,
    ServiceOrderItem,
    form=ServiceOrderItemForm,
    extra=0,
    can_delete=True,
    min_num=0,
    validate_min=False
)


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
