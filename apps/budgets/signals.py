"""
Signals for automatic service order creation from budgets.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Budget


def sync_service_order_items(budget):
    """
    Synchronise ServiceOrderItems from a budget's items.

    Called after budget items are saved so the Service Order mirrors the budget
    exactly, minus the financial values (unit_price / total_price are excluded).

    Existing ServiceOrderItems are matched by ``budget_item`` FK; items that no
    longer exist in the budget are deleted, and new items are created.
    Also updates the OS event if the project now has an event assigned.
    """
    from apps.service_orders.models import ServiceOrderItem

    try:
        service_order = budget.service_order
    except Exception:
        # ServiceOrder doesn't exist yet – nothing to sync
        return

    # Atualiza event na OS se o projeto ganhou evento após a criação do orçamento
    event = getattr(budget.proposal, 'event', None)
    if event is not None and service_order.event_id != event.pk:
        service_order.event = event
        service_order.save(update_fields=['event'])

    # Build a map of existing SO items keyed by their origin budget_item pk
    existing_by_budget_item = {
        soi.budget_item_id: soi
        for soi in service_order.items.filter(budget_item__isnull=False)
    }

    current_budget_item_ids = set()

    for budget_item in budget.items.select_related('section').all():
        current_budget_item_ids.add(budget_item.pk)

        section_name = budget_item.section.title if budget_item.section else None

        fields = dict(
            service_order=service_order,
            budget_item=budget_item,
            section_name=section_name,
            name=budget_item.name,
            description=budget_item.description,
            quantity=budget_item.quantity,
            dim_length=budget_item.dim_length,
            dim_width=budget_item.dim_width,
            dim_height=budget_item.dim_height,
            measurement=budget_item.measurement,
            measurement_unit=budget_item.measurement_unit,
            weight=budget_item.weight,
        )

        if budget_item.pk in existing_by_budget_item:
            # Update existing SO item
            soi = existing_by_budget_item[budget_item.pk]
            for attr, value in fields.items():
                setattr(soi, attr, value)
            soi.save()
        else:
            # Create new SO item
            ServiceOrderItem.objects.create(**fields)

    # Remove SO items whose origin budget_item no longer exists
    service_order.items.filter(
        budget_item__isnull=False
    ).exclude(
        budget_item_id__in=current_budget_item_ids
    ).delete()


@receiver(post_save, sender=Budget)
def create_service_order_on_budget_creation(sender, instance, created, **kwargs):
    """
    Automatically create a Service Order when a budget is created.
    
    This implements the business rule:
    New Budget -> Immediately create ServiceOrder
    """
    from apps.service_orders.models import ServiceOrder
    
    if created:
        event = getattr(instance.proposal, 'event', None)

        if not hasattr(instance, 'service_order'):
            ServiceOrder.objects.create(
                budget=instance,
                event=event,  # pode ser None se o projeto ainda não tem evento
                status='pending',
                created_by=instance.created_by,
            )

