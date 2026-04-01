"""
Dashboard views for the Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Single dashboard view. Superusers see the operations dashboard;
    financial users see the financial dashboard. Template is chosen at
    render time via get_template_names().
    """

    template_name = 'dashboard/home.html'

    def get_template_names(self):
        user = self.request.user
        if not user.is_superuser and user.is_financial:
            return ['dashboard/financial.html']
        return ['dashboard/home.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_superuser and user.is_financial:
            return self._financial_context(context)
        return self._main_context(context)

    # ------------------------------------------------------------------
    # Main dashboard context
    # ------------------------------------------------------------------
    def _main_context(self, context):
        from apps.events.models import Event
        from apps.projects.models import Project
        from apps.budgets.models import Budget
        from apps.service_orders.models import ServiceOrder
        from apps.technical_visits.models import TechnicalVisit

        today = timezone.now().date()
        next_month = today + timedelta(days=30)
        context['upcoming_events'] = Event.objects.filter(
            event_date__gte=today,
            event_date__lte=next_month
        )[:5]

        context['pending_projects'] = Project.objects.filter(
            status='in_development'
        ).count()

        context['approved_budgets'] = Budget.objects.filter(
            status='approved'
        ).count()

        context['active_service_orders'] = ServiceOrder.objects.filter(
            status='in_progress'
        ).count()

        context['scheduled_visits'] = TechnicalVisit.objects.filter(
            status='scheduled',
            visit_date__gte=timezone.now()
        ).count()

        context['total_events'] = Event.objects.count()

        now = timezone.now()
        current_month = now.month
        current_year = now.year
        context['budget_filter_year'] = current_year
        context['budget_filter_years'] = list(range(current_year - 4, current_year + 1))
        context['budget_approved_total'] = self._budget_total('approved', current_month, current_year)
        context['budget_sent_total'] = self._budget_total('sent', current_month, current_year)
        context['budget_rejected_total'] = self._budget_total('rejected', current_month, current_year)

        return context

    def _budget_total(self, status, month, year):
        """Calculate total monetary value of budgets with the given status for a month/year."""
        from apps.budgets.models import Budget
        result = Budget.objects.filter(
            status=status,
            created_at__year=year,
            created_at__month=month,
        ).aggregate(total=Sum('items__total_price'))['total']
        return float(result or 0)

    # ------------------------------------------------------------------
    # Financial dashboard context
    # ------------------------------------------------------------------
    def _financial_context(self, context):
        from apps.projects.models import Project
        from decimal import Decimal

        today = timezone.now().date()

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


class FinancialExportView(LoginRequiredMixin, TemplateView):
    """
    Standalone print-ready export of the financial dashboard.
    Accepts the same ?month=&year= filters as DashboardView.
    """

    template_name = 'dashboard/financial_export.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.projects.models import Project
        from decimal import Decimal

        today = timezone.now().date()

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
        context['month_choices'] = [
            (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
            (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
            (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
            (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro'),
        ]
        context['selected_month'] = month
        context['selected_year'] = year
        context['generated_at'] = timezone.now()
        return context


class ProjectTotalsView(LoginRequiredMixin, View):
    """
    AJAX endpoint returning summed budget values by status for a given month/year.
    """

    def get(self, request):
        now = timezone.now()
        try:
            month = int(request.GET.get('month', now.month))
            year = int(request.GET.get('year', now.year))
            if not (1 <= month <= 12):
                month = now.month
            if not (2000 <= year <= 2100):
                year = now.year
        except (ValueError, TypeError):
            month = now.month
            year = now.year

        from apps.budgets.models import Budget

        def get_total(status):
            result = Budget.objects.filter(
                status=status,
                created_at__year=year,
                created_at__month=month,
            ).aggregate(total=Sum('items__total_price'))['total']
            return float(result or 0)

        return JsonResponse({
            'approved': get_total('approved'),
            'sent': get_total('sent'),
            'rejected': get_total('rejected'),
            'month': month,
            'year': year,
        })

