"""
Forms for user authentication and management.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div

User = get_user_model()


class LoginForm(AuthenticationForm):
    """Custom login form with email instead of username."""
    
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
            'placeholder': 'seu@email.com'
        })
    )
    
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-black focus:ring-2 focus:ring-black/10 transition-all',
            'placeholder': '••••••••'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_show_labels = True


class UserCreationForm(BaseUserCreationForm):
    """Form for creating new users."""
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                Field('email', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
            Div(
                Field('first_name', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
            Div(
                Field('last_name', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
            Div(
                Field('phone', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
            Div(
                Field('password1', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
            Div(
                Field('password2', css_class='w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-black'),
                css_class='mb-4'
            ),
        )


class UserUpdateForm(forms.ModelForm):
    """Form for updating existing users."""
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
