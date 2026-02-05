"""
Signals for automatic service order creation from approved budgets.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Budget


@receiver(post_save, sender=Budget)
def create_service_order_on_approval(sender, instance, created, **kwargs):
    """
    Automatically create a Service Order when a budget is approved.
    
    This implements the core business rule:
    Budget.status = 'approved' -> Create ServiceOrder
    """
    # Import here to avoid circular imports
    from apps.service_orders.models import ServiceOrder
    
    # Only create service order if budget was just approved
    if instance.status == 'approved' and not created:
        # Check if service order already exists for this budget
        if not hasattr(instance, 'service_order'):
            # Create service order
            ServiceOrder.objects.create(
                budget=instance,
                event=instance.proposal.event,
                status='pending',
                created_by=instance.updated_by,
                updated_by=instance.updated_by
            )
