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
    Main dashboard view showing key metrics and upcoming events.
    """
    
    template_name = 'dashboard/home.html'
    
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
        
        # Pending projects (in_development = not yet approved or in execution)
        context['pending_proposals'] = Project.objects.filter(
            status='in_development'
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
        
        # Proposal totals for current month/year (initial render)
        now = timezone.now()
        current_month = now.month
        current_year = now.year
        context['proposal_filter_month'] = current_month
        context['proposal_filter_year'] = current_year
        context['proposal_filter_years'] = list(range(current_year - 4, current_year + 1))
        context['proposal_approved_total'] = self._proposal_total('approved', current_month, current_year)
        context['proposal_sent_total'] = self._proposal_total('sent', current_month, current_year)
        context['proposal_rejected_total'] = self._proposal_total('rejected', current_month, current_year)
        
        return context
    
    def _proposal_total(self, status, month, year):
        """Calculate total monetary value of budgets with the given status for a month/year."""
        from apps.budgets.models import Budget
        result = Budget.objects.filter(
            status=status,
            created_at__year=year,
            created_at__month=month,
        ).aggregate(total=Sum('items__total_price'))['total']
        return float(result or 0)


class ProposalTotalsView(LoginRequiredMixin, View):
    """
    AJAX endpoint returning summed proposal values by status for a given month/year.
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
