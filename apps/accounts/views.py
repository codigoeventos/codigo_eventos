"""
Views for user authentication and management.
"""

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from apps.common.mixins import AuditMixin, GroupRequiredMixin
from .models import User
from .forms import LoginForm, UserCreationForm, UserUpdateForm


class LoginView(BaseLoginView):
    """Custom login view using email authentication."""
    
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard:home')


def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('accounts:login')


class UserListView(GroupRequiredMixin, ListView):
    """List all users (admin only)."""
    
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    required_groups = ['Administrador']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset


class UserCreateView(GroupRequiredMixin, AuditMixin, CreateView):
    """Create a new user (admin only)."""
    
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    required_groups = ['Administrador']


class UserUpdateView(GroupRequiredMixin, AuditMixin, UpdateView):
    """Update an existing user (admin only)."""
    
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    required_groups = ['Administrador']


class UserDeleteView(GroupRequiredMixin, DeleteView):
    """Delete a user (admin only)."""
    
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user-list')
    required_groups = ['Administrador']
