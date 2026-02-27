"""
Budget forms for Event Management System.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Budget, BudgetItem


class BudgetForm(forms.ModelForm):
    """Form for creating and updating budgets."""
    
    class Meta:
        model = Budget
        fields = ['proposal', 'name', 'status']
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
        }
        labels = {
            'proposal': 'Proposta',
            'name': 'Nome',
            'status': 'Status',
        }


class BudgetItemForm(forms.ModelForm):
    """Form for budget items."""
    
    class Meta:
        model = BudgetItem
        fields = [
            'name', 'description', 'quantity',
            'dim_length', 'dim_width', 'dim_height',
            'measurement', 'measurement_unit',
            'weight', 'unit_price',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'item-name w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome do item'
            }),
            'description': forms.Textarea(attrs={
                'rows': 2,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Descrição do item'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'item-quantity w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'min': '1',
                'value': '1'
            }),
            'dim_length': forms.NumberInput(attrs={
                'class': 'item-dim w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.001', 'min': '0', 'placeholder': '0.000'
            }),
            'dim_width': forms.NumberInput(attrs={
                'class': 'item-dim w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.001', 'min': '0', 'placeholder': '0.000'
            }),
            'dim_height': forms.NumberInput(attrs={
                'class': 'item-dim w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.001', 'min': '0', 'placeholder': '0.000'
            }),
            'measurement': forms.NumberInput(attrs={
                'class': 'item-measurement w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent bg-gray-50',
                'step': '0.001', 'min': '0', 'placeholder': 'calculado automaticamente'
            }),
            'measurement_unit': forms.Select(attrs={
                'class': 'item-measurement-unit w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'item-weight w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.001', 'min': '0', 'placeholder': '0.000'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'item-unit-price w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'step': '0.01', 'min': '0', 'placeholder': '0.00'
            }),
        }
        labels = {
            'name': 'Item',
            'description': 'Descrição',
            'quantity': 'Quantidade',
            'dim_length': 'Comprimento (m)',
            'dim_width': 'Largura (m)',
            'dim_height': 'Altura (m)',
            'measurement': 'Volume (m³)',
            'measurement_unit': 'Unidade',
            'weight': 'Peso unitário (kg)',
            'unit_price': 'Preço Unitário (R$)',
        }


# Formset for budget items
BudgetItemFormSet = inlineformset_factory(
    Budget,
    BudgetItem,
    form=BudgetItemForm,
    extra=0,  # Number of empty forms to display
    can_delete=True,
    min_num=1,  # Minimum number of items required
    validate_min=True
)


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
        from apps.projects.models import Project
        self.fields['proposal'].queryset = Project.objects.all().order_by('-created_at')
