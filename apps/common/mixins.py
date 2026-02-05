"""
Common view mixins for the Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class AuditMixin:
    """
    Mixin to automatically set created_by and updated_by fields.
    
    Usage: Add to CreateView and UpdateView to track which user
    performed the action.
    """
    
    def form_valid(self, form):
        """Set the user fields before saving."""
        if hasattr(form.instance, 'created_by') and not form.instance.pk:
            form.instance.created_by = self.request.user
        if hasattr(form.instance, 'updated_by'):
            form.instance.updated_by = self.request.user
        return super().form_valid(form)


class PermissionRequiredMixin(LoginRequiredMixin):
    """
    Mixin to check if user has required permission.
    
    Usage:
        class MyView(PermissionRequiredMixin, ListView):
            permission_required = 'app.view_model'
    """
    
    permission_required = None
    
    def dispatch(self, request, *args, **kwargs):
        if self.permission_required:
            if not request.user.has_perm(self.permission_required):
                raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return super().dispatch(request, *args, **kwargs)


class GroupRequiredMixin(LoginRequiredMixin):
    """
    Mixin to check if user belongs to required group.
    
    Usage:
        class MyView(GroupRequiredMixin, ListView):
            required_groups = ['Administrador', 'Comercial']
    """
    
    required_groups = []
    
    def dispatch(self, request, *args, **kwargs):
        if self.required_groups:
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(group in user_groups for group in self.required_groups):
                raise PermissionDenied("Você não tem permissão para acessar esta página.")
        return super().dispatch(request, *args, **kwargs)
