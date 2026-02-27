"""
Budget views for Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from apps.common.mixins import AuditMixin
from .models import Budget, BudgetItem
from .forms import BudgetForm, BudgetSearchForm, BudgetItemFormSet

class BudgetListView(LoginRequiredMixin, ListView):
    """List all budgets with search and pagination."""
    
    model = Budget
    template_name = 'budgets/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 20
    
    def get_queryset(self):
        """Filter budgets based on search query."""
        queryset = Budget.objects.select_related('proposal', 'proposal__event', 'created_by', 'updated_by').all()
        
        # Search functionality
        search = self.request.GET.get('search', '').strip()
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(proposal__title__icontains=search) |
                Q(proposal__event__name__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status', '').strip()
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by proposal
        proposal = self.request.GET.get('proposal', '').strip()
        if proposal:
            queryset = queryset.filter(proposal_id=proposal)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        """Add search form and breadcrumbs to context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = BudgetSearchForm(self.request.GET)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': None}
        ]
        return context


class BudgetDetailView(LoginRequiredMixin, DetailView):
    """Display budget details and related data."""
    
    model = Budget
    template_name = 'budgets/budget_detail.html'
    context_object_name = 'budget'
    
    def get_queryset(self):
        """Optimize query with related objects."""
        return Budget.objects.select_related(
            'proposal',
            'proposal__event',
            'proposal__event__client',
            'created_by',
            'updated_by'
        ).prefetch_related(
            'items'
        )
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and related data to context."""
        from apps.logistics.models import UrgencyMultiplier
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': self.object.name, 'url': None}
        ]
        context['urgency_options'] = UrgencyMultiplier.objects.order_by('multiplier')
        return context


class BudgetCreateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, CreateView):
    """Create a new budget."""
    
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_message = "Orçamento %(name)s criado com sucesso!"
    
    def get_success_url(self):
        """Redirect to budget detail after creation."""
        return reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': 'Novo Orçamento', 'url': None}
        ]
        context['form_title'] = 'Novo Orçamento'
        context['submit_text'] = 'Criar Orçamento'
        
        from apps.logistics.models import UrgencyMultiplier
        context['urgency_options'] = UrgencyMultiplier.objects.order_by('multiplier')
        
        if self.request.POST:
            context['items_formset'] = BudgetItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = BudgetItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        """Save budget and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class BudgetUpdateView(LoginRequiredMixin, AuditMixin, SuccessMessageMixin, UpdateView):
    """Update an existing budget."""
    
    model = Budget
    form_class = BudgetForm
    template_name = 'budgets/budget_form.html'
    success_message = "Orçamento %(name)s atualizado com sucesso!"
    
    def get_success_url(self):
        """Redirect to budget detail after update."""
        return reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        """Add breadcrumbs and formset to context."""
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [
            {'name': 'Orçamentos', 'url': reverse_lazy('budgets:list')},
            {'name': self.object.name, 'url': reverse_lazy('budgets:detail', kwargs={'pk': self.object.pk})},
            {'name': 'Editar', 'url': None}
        ]
        context['form_title'] = f'Editar Orçamento: {self.object.name}'
        context['submit_text'] = 'Salvar Alterações'
        
        from apps.logistics.models import UrgencyMultiplier
        context['urgency_options'] = UrgencyMultiplier.objects.order_by('multiplier')
        
        if self.request.POST:
            context['items_formset'] = BudgetItemFormSet(self.request.POST, instance=self.object)
        else:
            context['items_formset'] = BudgetItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        """Save budget and items."""
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a budget (soft delete) - via AJAX only."""
    
    model = Budget
    success_url = reverse_lazy('budgets:list')
    success_message = "Orçamento excluído com sucesso!"
    
    def post(self, request, *args, **kwargs):
        """Handle POST delete request - AJAX only."""
        self.object = self.get_object()
        
        # Perform soft delete
        self.object.delete()
        
        # Return JSON response
        return JsonResponse({
            'success': True,
            'message': self.success_message
        })
    
    def get(self, request, *args, **kwargs):
        """Redirect GET requests to budget detail page."""
        budget = self.get_object()
        return HttpResponseRedirect(reverse_lazy('budgets:detail', kwargs={'pk': budget.pk}))


# Public Budget Approval Views

class PublicBudgetApprovalView(View):
    """
    Public view for clients to review and approve/reject budget.
    No login required - accessed via unique token.
    """
    template_name = 'budgets/public_approval.html'
    
    def get(self, request, token):
        """Display budget for approval."""
        budget = get_object_or_404(Budget, approval_token=token)
        
        # Get all items with their approval status
        items = budget.items.all()
        
        context = {
            'budget': budget,
            'items': items,
            'is_editable': budget.is_editable,
            'show_pdf_button': True,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, token):
        """Handle approval/rejection submission."""
        budget = get_object_or_404(Budget, approval_token=token)
        
        # Check if budget can still be edited
        if not budget.is_editable:
            messages.error(request, 'Este orçamento já foi processado e não pode mais ser modificado.')
            return redirect('budgets:public_approval', token=token)
        
        action = request.POST.get('action')
        
        if action == 'approve':
            # Get selected items
            selected_items = request.POST.getlist('items')
            
            # Update approval status for all items
            for item in budget.items.all():
                item.is_approved = str(item.id) in selected_items
                item.save()
            
            # Update budget status
            budget.approval_status = 'approved'
            budget.approved_at = timezone.now()
            budget.client_notes = request.POST.get('notes', '')
            budget.status = 'approved'
            budget.save()
            
            messages.success(request, 'Orçamento aprovado com sucesso!')
            
        elif action == 'reject':
            # Mark budget as rejected
            budget.approval_status = 'rejected'
            budget.approved_at = timezone.now()
            budget.client_notes = request.POST.get('notes', '')
            budget.status = 'rejected'
            budget.save()
            
            messages.info(request, 'Orçamento rejeitado.')
        
        return redirect('budgets:public_approval', token=token)


class PublicBudgetPDFView(View):
    """Generate PDF for budget - public access via token."""
    
    def get(self, request, token):
        """Generate and return PDF."""
        budget = get_object_or_404(Budget, approval_token=token)
        
        # Import here to avoid issues if reportlab not installed yet
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib import colors
            from reportlab.lib.units import cm
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from django.http import HttpResponse
            from io import BytesIO
        except ImportError:
            messages.error(request, 'Sistema de geração de PDF não está disponível.')
            return redirect('budgets:public_approval', token=token)
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#000000'),
            spaceAfter=30,
        )
        elements.append(Paragraph(f'Orçamento: {budget.name}', title_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Budget info
        info_style = styles['Normal']
        elements.append(Paragraph(f'<b>Projeto:</b> {budget.proposal.title}', info_style))
        elements.append(Paragraph(f'<b>Status:</b> {budget.get_approval_status_display()}', info_style))
        if budget.approved_at:
            elements.append(Paragraph(f'<b>Data de Aprovação:</b> {budget.approved_at.strftime("%d/%m/%Y %H:%M")}', info_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Items table
        table_data = [['Item', 'Qtd', 'Valor Unit.', 'Total', 'Status']]
        
        for item in budget.items.all():
            status = 'Aprovado' if item.is_approved else 'Não Aprovado'
            if budget.is_editable:
                status = 'Pendente'
            
            table_data.append([
                item.name,
                str(item.quantity),
                f'R$ {item.unit_price:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                f'R$ {item.total_price:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                status
            ])
        
        # Total row
        total = budget.approved_value if not budget.is_editable else budget.total_value
        table_data.append(['', '', '', f'R$ {total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), ''])
        
        table = Table(table_data, colWidths=[8*cm, 2*cm, 3*cm, 3*cm, 3*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)
        
        # Client notes
        if budget.client_notes:
            elements.append(Spacer(1, 0.5*cm))
            elements.append(Paragraph('<b>Observações do Cliente:</b>', styles['Heading2']))
            elements.append(Paragraph(budget.client_notes, info_style))
        
        # Build PDF
        doc.build(elements)
        
        # Return response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="orcamento_{budget.id}.pdf"'
        
        return response


# ── Freight Calculation ─────────────────────────────────────────────────────

class BudgetCalculateFreightView(LoginRequiredMixin, View):
    """
    Calculate (or recalculate) freight for a budget and save the result.

    POST params (all optional):
        urgency_id   – pk of UrgencyMultiplier to use
        distance_km  – delivery distance in km
        save         – "1" to persist freight_cost on the budget
    Returns JSON with the full breakdown.
    """

    def post(self, request, pk):
        from apps.logistics.models import UrgencyMultiplier
        from apps.logistics.utils import calculate_freight
        from decimal import Decimal, InvalidOperation

        budget = get_object_or_404(Budget, pk=pk)

        urgency = None
        urgency_id = request.POST.get('urgency_id') or ''
        if urgency_id.isdigit():
            urgency = UrgencyMultiplier.objects.filter(pk=int(urgency_id)).first()

        distance_km = None
        raw_distance = request.POST.get('distance_km') or ''
        try:
            distance_km = Decimal(raw_distance) if raw_distance else None
        except InvalidOperation:
            pass

        result = calculate_freight(budget, urgency=urgency, distance_km=distance_km)

        # Persist if requested
        should_save = request.POST.get('save') == '1'
        if should_save:
            budget.freight_cost = result['freight_total']
            budget.freight_urgency = urgency
            if distance_km is not None:
                budget.freight_distance_km = distance_km
            budget.save(update_fields=['freight_cost', 'freight_urgency', 'freight_distance_km'])
            messages.success(request, f"Frete calculado e salvo: R$ {result['freight_total']:.2f}")

        # Return JSON for AJAX or redirect for standard form
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'weight_total': float(result['weight_total']),
                'volume_total': float(result['volume_total']),
                'weight_cost': float(result['weight_cost']),
                'volume_cost': float(result['volume_cost']),
                'base_freight': float(result['base_freight']),
                'fixed_fee': float(result['fixed_fee']),
                'percentage_cost': float(result['percentage_cost']),
                'distance_cost': float(result['distance_cost']),
                'urgency_multiplier': float(result['urgency_multiplier']),
                'urgency_label': result['urgency_label'],
                'freight_total': float(result['freight_total']),
            })

        return redirect('budgets:detail', pk=pk)


# ── Freight Live Preview (no save) ──────────────────────────────────────────

class BudgetFreightPreviewView(LoginRequiredMixin, View):
    """
    AJAX-only endpoint.  Accepts live item data from the budget form and
    returns a freight breakdown WITHOUT touching the database.

    POST body (application/x-www-form-urlencoded or JSON):
        items_json   – JSON array of objects:
                        {weight, volume, quantity, measurement_unit}
        budget_total – float – sum of all item totals
        urgency_id   – int (optional)
        distance_km  – float (optional)
    """

    def post(self, request):
        import json
        from decimal import Decimal, InvalidOperation
        from apps.logistics.models import FreightSettings, UrgencyMultiplier, WeightRange, VolumeRange
        from apps.logistics.utils import _weight_cost, _volume_cost

        # ── Parse payload ──────────────────────────────────────────────────
        try:
            items = json.loads(request.POST.get('items_json', '[]'))
        except (ValueError, TypeError):
            items = []

        try:
            budget_total = Decimal(str(request.POST.get('budget_total', '0')))
        except InvalidOperation:
            budget_total = Decimal('0')

        urgency_id = request.POST.get('urgency_id', '').strip()
        urgency = None
        if urgency_id.isdigit():
            urgency = UrgencyMultiplier.objects.filter(pk=int(urgency_id)).first()
        if urgency is None:
            urgency = UrgencyMultiplier.objects.filter(is_default=True).first()

        distance_km = None
        raw_dist = request.POST.get('distance_km', '').strip()
        try:
            distance_km = Decimal(raw_dist) if raw_dist else None
        except InvalidOperation:
            pass

        # ── Aggregate weight & volume from item list ───────────────────────
        weight_total = Decimal('0')
        volume_total = Decimal('0')

        for item in items:
            try:
                qty = Decimal(str(item.get('quantity', 1) or 1))
                w = item.get('weight') or 0
                v = item.get('volume') or 0
                mu = item.get('measurement_unit', '') or ''

                if w:
                    weight_total += Decimal(str(w)) * qty
                if v and mu == 'm3':
                    volume_total += Decimal(str(v)) * qty
            except (InvalidOperation, TypeError):
                continue

        # ── Cost per table ─────────────────────────────────────────────────
        settings = FreightSettings.get_settings()
        w_cost = _weight_cost(weight_total)
        v_cost = _volume_cost(volume_total)

        mode = settings.calculation_mode
        if mode == 'max':
            base_freight = max(w_cost, v_cost)
        elif mode == 'sum':
            base_freight = w_cost + v_cost
        elif mode == 'weight':
            base_freight = w_cost
        else:
            base_freight = v_cost

        fixed_fee = settings.fixed_delivery_fee or Decimal('0')
        pct = settings.percentage_on_total or Decimal('0')
        percentage_cost = budget_total * (pct / Decimal('100'))

        distance_cost = Decimal('0')
        if settings.distance_rate_enabled and distance_km is not None:
            distance_cost = settings.distance_rate_per_km * distance_km

        urgency_multiplier = urgency.multiplier if urgency else Decimal('1')
        urgency_label = urgency.label if urgency else 'Normal'

        freight_sub = base_freight + fixed_fee + percentage_cost + distance_cost
        freight_total = freight_sub * urgency_multiplier

        return JsonResponse({
            'weight_total': float(weight_total),
            'volume_total': float(volume_total),
            'weight_cost': float(w_cost),
            'volume_cost': float(v_cost),
            'base_freight': float(base_freight),
            'fixed_fee': float(fixed_fee),
            'percentage_cost': float(percentage_cost),
            'distance_cost': float(distance_cost),
            'urgency_multiplier': float(urgency_multiplier),
            'urgency_label': urgency_label,
            'freight_total': float(freight_total),
        })
