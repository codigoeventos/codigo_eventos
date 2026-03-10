"""
Dashboard views for the Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta

from apps.common.mixins import GroupRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view. Financial group users are redirected to the
    financial dashboard; all other users see the standard dashboard.
    """

    template_name = 'dashboard/home.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_financial:
            from django.shortcuts import redirect
            return redirect('dashboard:financial')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Import models here to avoid circular imports
        from apps.events.models import Event
        from apps.projects.models import Project
        from apps.budgets.models import Budget
        from apps.service_orders.models import ServiceOrder
        from apps.technical_visits.models import TechnicalVisit

        # Upcoming events (next 30 days)
        today = timezone.now().date()
        next_month = today + timedelta(days=30)
        context['upcoming_events'] = Event.objects.filter(
            event_date__gte=today,
            event_date__lte=next_month
        )[:5]

        # Pending projects
        context['pending_proposals'] = Project.objects.filter(
            status='sent'
        ).count()

        # Approved budgets
        context['approved_budgets'] = Budget.objects.filter(
            status='approved'
        ).count()

        # Active service orders
        context['active_service_orders'] = ServiceOrder.objects.filter(
            status='in_progress'
        ).count()

        # Scheduled technical visits
        context['scheduled_visits'] = TechnicalVisit.objects.filter(
            status='scheduled',
            visit_date__gte=timezone.now()
        ).count()

        # Recent events count
        context['total_events'] = Event.objects.count()

        return context


class FinancialDashboardView(GroupRequiredMixin, TemplateView):
    """
    Financial dashboard showing project values, contractor spend and profit.
    Accessible only to users in the 'Financeiro' group (and superusers).
    Supports filtering by month and year based on project creation date.
    """

    template_name = 'dashboard/financial.html'
    required_groups = ['Financeiro']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from apps.projects.models import Project
        from decimal import Decimal

        today = timezone.now().date()

        # Read filter params
        try:
            month = int(self.request.GET.get('month', ''))
        except (ValueError, TypeError):
            month = None
        try:
            year = int(self.request.GET.get('year', ''))
        except (ValueError, TypeError):
            year = None

        projects = Project.objects.select_related(
            'event', 'contractor'
        ).prefetch_related('budgets__items')

        if month:
            projects = projects.filter(created_at__month=month)
        if year:
            projects = projects.filter(created_at__year=year)

        # Build rows with calculated fields
        rows = []
        total_project_value = Decimal('0')
        total_contractor_spend = Decimal('0')
        total_profit = Decimal('0')

        for project in projects:
            pv = Decimal(str(project.total_value))
            cs = project.contractor_spend or Decimal('0')
            profit = pv - cs
            total_project_value += pv
            total_contractor_spend += cs
            total_profit += profit
            rows.append({
                'project': project,
                'total_value': pv,
                'contractor_spend': cs,
                'profit': profit,
            })

        context['rows'] = rows
        context['total_project_value'] = total_project_value
        context['total_contractor_spend'] = total_contractor_spend
        context['total_profit'] = total_profit

        # Year choices for filter dropdown (all years that have projects)
        context['year_choices'] = Project.objects.dates('created_at', 'year')
        context['month_choices'] = [
            (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
            (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
            (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
            (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
        ]
        context['selected_month'] = month
        context['selected_year'] = year
        context['current_year'] = today.year

        return context

