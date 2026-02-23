"""
Dashboard views for the Event Management System.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
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
