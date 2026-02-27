"""
Views for the Logistics / Freight configuration panel.

URL namespace: logistics
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView, View,
)
from django.shortcuts import redirect, render

from .forms import (
    FreightSettingsForm,
    UrgencyMultiplierForm,
    VolumeRangeForm,
    WeightRangeForm,
)
from .models import FreightSettings, UrgencyMultiplier, VolumeRange, WeightRange


# ── Freight Settings (singleton) ────────────────────────────────────────────

class FreightSettingsView(LoginRequiredMixin, View):
    """Display and update the global freight settings."""

    template_name = 'logistics/config.html'

    def get(self, request):
        instance = FreightSettings.get_settings()
        form = FreightSettingsForm(instance=instance)
        context = self._base_context(form)
        return render(request, self.template_name, context)

    def post(self, request):
        instance = FreightSettings.get_settings()
        form = FreightSettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configurações de frete salvas com sucesso!')
            return redirect('logistics:config')
        context = self._base_context(form)
        return render(request, self.template_name, context)

    def _base_context(self, form):
        return {
            'form': form,
            'weight_ranges': WeightRange.objects.all(),
            'volume_ranges': VolumeRange.objects.all(),
            'urgency_multipliers': UrgencyMultiplier.objects.all(),
            'breadcrumbs': [
                {'name': 'Configurações', 'url': None},
                {'name': 'Logística e Frete', 'url': None},
            ],
        }


# ── Weight Ranges ────────────────────────────────────────────────────────────

class WeightRangeCreateView(LoginRequiredMixin, CreateView):
    model = WeightRange
    form_class = WeightRangeForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Nova Faixa de Peso'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Nova Faixa de Peso', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de peso criada com sucesso!')
        return super().form_valid(form)


class WeightRangeUpdateView(LoginRequiredMixin, UpdateView):
    model = WeightRange
    form_class = WeightRangeForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'Editar Faixa de Peso – {self.object.label}'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Editar Faixa de Peso', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de peso atualizada com sucesso!')
        return super().form_valid(form)


class WeightRangeDeleteView(LoginRequiredMixin, DeleteView):
    model = WeightRange
    success_url = reverse_lazy('logistics:config')

    def get(self, request, *args, **kwargs):
        # Perform delete on GET (called via JS confirm)
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de peso removida.')
        return super().form_valid(form)


# ── Volume Ranges ────────────────────────────────────────────────────────────

class VolumeRangeCreateView(LoginRequiredMixin, CreateView):
    model = VolumeRange
    form_class = VolumeRangeForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Nova Faixa de Volume'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Nova Faixa de Volume', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de volume criada com sucesso!')
        return super().form_valid(form)


class VolumeRangeUpdateView(LoginRequiredMixin, UpdateView):
    model = VolumeRange
    form_class = VolumeRangeForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'Editar Faixa de Volume – {self.object.label}'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Editar Faixa de Volume', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de volume atualizada com sucesso!')
        return super().form_valid(form)


class VolumeRangeDeleteView(LoginRequiredMixin, DeleteView):
    model = VolumeRange
    success_url = reverse_lazy('logistics:config')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Faixa de volume removida.')
        return super().form_valid(form)


# ── Urgency Multipliers ──────────────────────────────────────────────────────

class UrgencyCreateView(LoginRequiredMixin, CreateView):
    model = UrgencyMultiplier
    form_class = UrgencyMultiplierForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = 'Nova Urgência de Entrega'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Nova Urgência', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Urgência criada com sucesso!')
        return super().form_valid(form)


class UrgencyUpdateView(LoginRequiredMixin, UpdateView):
    model = UrgencyMultiplier
    form_class = UrgencyMultiplierForm
    template_name = 'logistics/range_form.html'
    success_url = reverse_lazy('logistics:config')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_title'] = f'Editar Urgência – {self.object.label}'
        ctx['cancel_url'] = reverse_lazy('logistics:config')
        ctx['breadcrumbs'] = [
            {'name': 'Logística e Frete', 'url': reverse_lazy('logistics:config')},
            {'name': 'Editar Urgência', 'url': None},
        ]
        return ctx

    def form_valid(self, form):
        messages.success(self.request, 'Urgência atualizada com sucesso!')
        return super().form_valid(form)


class UrgencyDeleteView(LoginRequiredMixin, DeleteView):
    model = UrgencyMultiplier
    success_url = reverse_lazy('logistics:config')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Urgência removida.')
        return super().form_valid(form)
