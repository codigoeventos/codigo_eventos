"""
Views for user authentication and management.
"""

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from apps.common.mixins import AuditMixin, GroupRequiredMixin
from .models import User
from .forms import LoginForm, UserCreationForm, UserUpdateForm, ChangePasswordForm


class LoginView(BaseLoginView):
    """Custom login view using email authentication."""
    
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # Check if user must change password
        if self.request.user.must_change_password:
            return reverse_lazy('accounts:change-password')
        return reverse_lazy('dashboard:home')


class ChangePasswordView(LoginRequiredMixin, FormView):
    """View for users to change their password on first login."""
    
    form_class = ChangePasswordForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('dashboard:home')
    
    def dispatch(self, request, *args, **kwargs):
        # Only allow access if user must change password
        if not request.user.must_change_password:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.save()
        # Update session to prevent logout after password change
        update_session_auth_hash(self.request, self.request.user)
        messages.success(self.request, 'Senha alterada com sucesso!')
        return super().form_valid(form)


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


class UserCreateView(GroupRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new user (admin only)."""
    
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    success_message = "Usuário %(email)s criado com sucesso!"
    required_groups = ['Administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Novo Usuário'
        context['submit_text'] = 'Criar Usuário'
        return context


class UserUpdateView(GroupRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing user (admin only)."""
    
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user-list')
    success_message = "Usuário %(email)s atualizado com sucesso!"
    required_groups = ['Administrador']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = f'Editar Usuário: {self.object.email}'
        context['submit_text'] = 'Salvar Alterações'
        return context
    
    def form_valid(self, form):
        # If editing own account and password changed, update session
        response = super().form_valid(form)
        if self.request.user.pk == self.object.pk:
            if form.cleaned_data.get('new_password') or form.cleaned_data.get('reset_password'):
                update_session_auth_hash(self.request, self.object)
        return response
        context['submit_text'] = 'Salvar Alterações'
        return context


class UserDeleteView(GroupRequiredMixin, DeleteView):
    """Delete a user (admin only)."""
    
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user-list')
    required_groups = ['Administrador']
