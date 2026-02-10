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


class UserCreationForm(forms.ModelForm):
    """Form for creating new users with default password."""
    
    groups = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Grupos'
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'groups', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'usuario@email.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Sobrenome'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
        }
        labels = {
            'email': 'Email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'is_active': 'Ativo',
            'is_staff': 'Acesso ao Admin',
            'is_superuser': 'Superusuário',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import Group
        self.fields['groups'].queryset = Group.objects.all()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Set default password to "123"
        user.set_password('123')
        # Force password change on first login
        user.must_change_password = True
        if commit:
            user.save()
            # Save many-to-many relationships
            self.save_m2m()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating existing users."""
    
    groups = forms.ModelMultipleChoiceField(
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Grupos'
    )
    
    new_password = forms.CharField(
        required=False,
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': 'Deixe em branco para não alterar'
        }),
        help_text='Deixe em branco se não quiser alterar a senha. Mínimo de 8 caracteres.'
    )
    
    reset_password = forms.BooleanField(
        required=False,
        label='Redefinir senha para "123"',
        widget=forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
        help_text='Marque para redefinir a senha para "123" e forçar mudança no próximo login.'
    )
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'groups', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'usuario@email.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Nome'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
                'placeholder': 'Sobrenome'
            }),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-black focus:ring-black'}),
        }
        labels = {
            'email': 'Email',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'is_active': 'Ativo',
            'is_staff': 'Acesso ao Admin',
            'is_superuser': 'Superusuário',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import Group
        self.fields['groups'].queryset = Group.objects.all()
        if self.instance and self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        reset_password = cleaned_data.get('reset_password')
        
        # Can't use both options at once
        if new_password and reset_password:
            raise forms.ValidationError('Escolha apenas uma opção: definir nova senha OU redefinir para 123.')
        
        # Validate password length if provided
        if new_password and len(new_password) < 8:
            self.add_error('new_password', 'A senha deve ter pelo menos 8 caracteres.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Handle password reset to "123"
        if self.cleaned_data.get('reset_password'):
            user.set_password('123')
            user.must_change_password = True
        # Handle custom password
        elif self.cleaned_data.get('new_password'):
            user.set_password(self.cleaned_data['new_password'])
            user.must_change_password = False
        
        if commit:
            user.save()
            self.save_m2m()
        return user


class ChangePasswordForm(forms.Form):
    """Form for users to change their password on first login."""
    
    old_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': '••••••••'
        })
    )
    
    new_password1 = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': '••••••••'
        }),
        help_text='A senha deve ter pelo menos 8 caracteres.'
    )
    
    new_password2 = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent',
            'placeholder': '••••••••'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Senha atual incorreta.')
        return old_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError('As senhas não coincidem.')
            if len(new_password1) < 8:
                raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres.')
        
        return cleaned_data
    
    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.must_change_password = False
        self.user.save()
        return self.user
