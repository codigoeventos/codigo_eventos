"""
Custom User model with email-based authentication.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom manager for User model with email as the unique identifier.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with the given email and password."""
        if not email:
            raise ValueError(_('O endereço de e-mail deve ser fornecido'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser deve ter is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser deve ter is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of username for authentication.
    
    Fields:
        email: Unique email address (used for login)
        first_name: User's first name
        last_name: User's last name
        phone: Optional phone number
        is_active: Boolean flag for account activation
        is_staff: Boolean flag for admin access
        created_at: Timestamp when user was created
    """
    
    email = models.EmailField(
        _('e-mail'),
        unique=True,
        help_text=_('Endereço de e-mail único para login'),
        error_messages={
            'unique': _('Já existe um usuário com este e-mail.'),
        }
    )
    
    first_name = models.CharField(
        _('primeiro nome'),
        max_length=150
    )
    
    last_name = models.CharField(
        _('sobrenome'),
        max_length=150
    )
    
    phone = models.CharField(
        _('telefone'),
        max_length=20,
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(
        _('ativo'),
        default=True,
        help_text=_('Desmarque para desativar o usuário ao invés de excluí-lo.')
    )
    
    is_staff = models.BooleanField(
        _('membro da equipe'),
        default=False,
        help_text=_('Permite que o usuário acesse o admin.')
    )
    
    created_at = models.DateTimeField(
        _('criado em'),
        auto_now_add=True
    )
    
    must_change_password = models.BooleanField(
        _('deve alterar senha'),
        default=False,
        help_text=_('Força o usuário a alterar a senha no próximo login.')
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')
        ordering = ['-created_at']
    
    def __str__(self):
        """String representation of the user."""
        return self.email
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """Return the user's first name."""
        return self.first_name
