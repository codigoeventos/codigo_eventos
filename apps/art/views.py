"""
ART (Anotação de Responsabilidade Técnica) views.
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView

from apps.projects.models import Project
from .models import ART
from .forms import ARTEditForm


class ARTGenerateView(LoginRequiredMixin, View):
    """
    Generates an ART automatically from project + budget data.

    GET  → confirmation page showing what will be generated.
    POST → creates the ART and redirects to the detail page.

    Rules:
    - Project must have at least one budget.
    - Only one ART per project (OneToOne). If one already exists, redirect to it.
    - All data is derived automatically; no manual form required.
    """

    def _get_project(self, pk):
        return get_object_or_404(
            Project.objects.select_related('event', 'event__client', 'contractor')
                           .prefetch_related('budgets', 'budgets__items'),
            pk=pk,
        )

    def _guard(self, request, project):
        """Return a redirect response if ART cannot be created, else None."""
        if not project.budgets.exists():
            messages.error(request, 'Não é possível gerar uma ART sem um orçamento vinculado ao projeto.')
            return redirect('projects:detail', pk=project.pk)
        try:
            existing = project.art
            messages.info(request, 'Este projeto já possui uma ART.')
            return redirect('art:detail', pk=existing.pk)
        except ART.DoesNotExist:
            pass
        return None

    def _build_art_data(self, project):
        """Derive all ART fields automatically from project / budget."""
        quantity = ART.calculate_quantity(project)
        if not quantity:
            quantity = Decimal('0')

        location = ''
        start_date = None
        end_date = None
        if project.event:
            location = project.event.location or ''
            end_date = project.event.event_date

        # Activity description: project title + description (if any)
        activity_parts = [project.title]
        if project.description:
            activity_parts.append(project.description)
        activity_description = '\n'.join(activity_parts)

        contract_value = project.total_value or Decimal('0')

        return {
            'quantity': quantity,
            'location': location,
            'activity_description': activity_description,
            'contract_value': contract_value,
            'start_date': start_date,
            'end_date': end_date,
        }

    def post(self, request, project_pk):
        project = self._get_project(project_pk)
        guard = self._guard(request, project)
        if guard:
            return guard

        data = self._build_art_data(project)

        art = ART.objects.create(
            project=project,
            activity_description=data['activity_description'],
            location=data['location'],
            quantity=data['quantity'],
            measurement_unit='m3',
            contract_value=data['contract_value'] if data['contract_value'] else None,
            start_date=data['start_date'],
            end_date=data['end_date'],
            created_by=request.user,
            updated_by=request.user,
        )

        messages.success(request, f'ART {art.art_number} gerada com sucesso!')
        return redirect('art:detail', pk=art.pk)


class ARTDetailView(LoginRequiredMixin, DetailView):
    """Internal detail view for an ART (authenticated)."""

    model = ART
    template_name = 'art/art_detail.html'
    context_object_name = 'art'

    def get_queryset(self):
        return ART.objects.select_related(
            'project',
            'project__event',
            'project__event__client',
            'created_by',
            'updated_by',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': reverse_lazy('projects:list')},
            {'name': self.object.project.title, 'url': reverse_lazy('projects:detail', kwargs={'pk': self.object.project.pk})},
            {'name': self.object.art_number, 'url': None},
        ]
        return context


class PublicARTView(View):
    """
    Public (unauthenticated) view of an ART, accessible via UUID token.
    Renders a print-friendly HTML page (same pattern as OS public view).
    """

    def get(self, request, token):
        art = get_object_or_404(
            ART.objects.select_related(
                'project',
                'project__event',
                'project__event__client',
                'created_by',
            ),
            public_token=token,
        )
        return render(request, 'art/public_art.html', {'art': art})


class ARTUpdateView(LoginRequiredMixin, UpdateView):
    """Edit engineer data and other ART fields after auto-generation."""

    model = ART
    form_class = ARTEditForm
    template_name = 'art/art_edit.html'
    context_object_name = 'art'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Projetos', 'url': reverse_lazy('projects:list')},
            {'name': self.object.project.title, 'url': reverse_lazy('projects:detail', kwargs={'pk': self.object.project.pk})},
            {'name': self.object.art_number, 'url': reverse_lazy('art:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None},
        ]
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'ART atualizada com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('art:detail', kwargs={'pk': self.object.pk})


class ARTDeleteView(LoginRequiredMixin, View):
    """Delete an ART (redirects back to project)."""

    def post(self, request, pk):
        art = get_object_or_404(ART, pk=pk)
        project_pk = art.project.pk
        art.delete()
        messages.success(request, 'ART excluída com sucesso.')
        return redirect('projects:detail', pk=project_pk)
