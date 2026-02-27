"""
Signals for automatic service order creation from budgets.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Budget


@receiver(post_save, sender=Budget)
def create_service_order_on_budget_creation(sender, instance, created, **kwargs):
    """
    Automatically create a Service Order when a budget is created.
    
    This implements the business rule:
    New Budget -> Immediately create ServiceOrder
    """
    # Import here to avoid circular imports
    from apps.service_orders.models import ServiceOrder
    
    # Create service order immediately when budget is created
    if created:
        # Check if service order doesn't already exist
        if not hasattr(instance, 'service_order'):
            # Create service order
            ServiceOrder.objects.create(
                budget=instance,
                event=instance.proposal.event,
                status='pending',
                created_by=instance.created_by,
            )

