"""
Project forms for Event Management System.
"""

from django import forms
from .models import Project, ProjectFile


CSS_INPUT = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent'
CSS_FILE = 'w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-medium file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200'


class ProjectForm(forms.ModelForm):
    """Form for creating and updating projects."""

    class Meta:
        model = Project
        fields = ['event', 'title', 'description', 'status', 'contractor', 'original_document']
        widgets = {
            'event': forms.Select(attrs={'class': CSS_INPUT}),
            'title': forms.TextInput(attrs={
                'class': CSS_INPUT,
                'placeholder': 'Título do projeto'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': CSS_INPUT,
                'placeholder': 'Descrição detalhada do projeto'
            }),
            'status': forms.Select(attrs={'class': CSS_INPUT}),
            'contractor': forms.Select(attrs={'class': CSS_INPUT}),
            'original_document': forms.FileInput(attrs={'class': CSS_FILE}),
        }
        labels = {
            'event': 'Evento',
            'title': 'Título',
            'description': 'Descrição',
            'status': 'Status',
            'contractor': 'Empreiteira Responsável',
            'original_document': 'Documento Original',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.contractors.models import Contractor
        self.fields['contractor'].queryset = Contractor.objects.all().order_by('name')
        self.fields['contractor'].empty_label = '— Nenhuma empreiteira —'
        self.fields['contractor'].required = False


class ProjectFileForm(forms.ModelForm):
    """Form for uploading a file to a project."""

    class Meta:
        model = ProjectFile
        fields = ['name', 'file', 'file_type', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': CSS_INPUT,
                'placeholder': 'Ex: Planta baixa pavimento térreo'
            }),
            'file': forms.FileInput(attrs={'class': CSS_FILE}),
            'file_type': forms.Select(attrs={'class': CSS_INPUT}),
            'notes': forms.TextInput(attrs={
                'class': CSS_INPUT,
                'placeholder': 'Observações opcionais'
            }),
        }
        labels = {
            'name': 'Nome',
            'file': 'Arquivo',
            'file_type': 'Tipo',
            'notes': 'Observações',
        }


class ProjectSearchForm(forms.Form):
    """Form for searching projects."""

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Buscar projetos...'
        })
    )

    status = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os status')] + Project.STATUS_CHOICES,
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
