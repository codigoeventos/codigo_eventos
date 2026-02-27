"""
Freight calculation utilities.

calculate_freight(budget, urgency=None, distance_km=None)
    Returns a dict with:
        weight_total      – total kg from budget items
        volume_total      – total m³ from budget items (m3 unit only)
        weight_cost       – cost from weight table
        volume_cost       – cost from volume table
        base_freight      – combined cost according to calculation_mode
        fixed_fee         – FreightSettings.fixed_delivery_fee
        percentage_cost   – percentage over budget total
        distance_cost     – optional distance cost
        urgency_multiplier– multiplier applied
        freight_total     – final freight cost
"""

from decimal import Decimal
from .models import FreightSettings, UrgencyMultiplier, VolumeRange, WeightRange


def _weight_cost(weight_kg: Decimal) -> Decimal:
    """Return shipping cost for the given weight in kg."""
    ranges = WeightRange.objects.order_by('order', 'min_weight')
    if not ranges.exists():
        return Decimal('0')

    for r in ranges:
        in_range = weight_kg >= r.min_weight and (
            r.max_weight is None or weight_kg <= r.max_weight
        )
        if in_range:
            if r.rate_type == 'per_ton':
                excess_kg = weight_kg - r.min_weight
                return r.rate * (excess_kg / Decimal('1000'))
            return r.rate

    # Fallback: use last range
    last = ranges.last()
    if last:
        if last.rate_type == 'per_ton':
            excess_kg = weight_kg - last.min_weight
            return last.rate * (excess_kg / Decimal('1000'))
        return last.rate
    return Decimal('0')


def _volume_cost(volume_m3: Decimal) -> Decimal:
    """Return shipping cost for the given volume in m³."""
    ranges = VolumeRange.objects.order_by('order', 'min_volume')
    if not ranges.exists():
        return Decimal('0')

    for r in ranges:
        in_range = volume_m3 >= r.min_volume and (
            r.max_volume is None or volume_m3 <= r.max_volume
        )
        if in_range:
            if r.rate_type == 'per_m3':
                excess = volume_m3 - r.min_volume
                return r.rate * excess
            return r.rate

    # Fallback: use last range
    last = ranges.last()
    if last:
        if last.rate_type == 'per_m3':
            excess = volume_m3 - last.min_volume
            return last.rate * excess
        return last.rate
    return Decimal('0')


def calculate_freight(budget, urgency=None, distance_km=None):
    """
    Calculate freight cost for a Budget instance.

    Parameters
    ----------
    budget      : Budget model instance
    urgency     : UrgencyMultiplier instance or None
    distance_km : Decimal/float – distance in km (optional)

    Returns
    -------
    dict with all breakdown fields and freight_total
    """
    settings = FreightSettings.get_settings()

    # ── Aggregate weight and volume from budget items ──────────────────────
    weight_total = Decimal('0')
    volume_total = Decimal('0')

    for item in budget.items.all():
        quantity = Decimal(str(item.quantity or 1))

        if item.weight:
            weight_total += item.weight * quantity

        # Volume: only items with measurement_unit == 'm3'
        if item.measurement and item.measurement_unit == 'm3':
            volume_total += item.measurement * quantity

    # ── Cost per table ─────────────────────────────────────────────────────
    w_cost = _weight_cost(weight_total)
    v_cost = _volume_cost(volume_total)

    mode = settings.calculation_mode
    if mode == 'max':
        base_freight = max(w_cost, v_cost)
    elif mode == 'sum':
        base_freight = w_cost + v_cost
    elif mode == 'weight':
        base_freight = w_cost
    else:  # 'volume'
        base_freight = v_cost

    # ── Fixed fee ──────────────────────────────────────────────────────────
    fixed_fee = settings.fixed_delivery_fee or Decimal('0')

    # ── Percentage over budget total ───────────────────────────────────────
    budget_total = Decimal(str(budget.total_value))
    pct = settings.percentage_on_total or Decimal('0')
    percentage_cost = budget_total * (pct / Decimal('100'))

    # ── Distance cost ──────────────────────────────────────────────────────
    distance_cost = Decimal('0')
    if settings.distance_rate_enabled and distance_km is not None:
        distance_cost = settings.distance_rate_per_km * Decimal(str(distance_km))

    # ── Urgency multiplier ─────────────────────────────────────────────────
    if urgency is None:
        urgency = UrgencyMultiplier.objects.filter(is_default=True).first()

    urgency_multiplier = urgency.multiplier if urgency else Decimal('1')

    freight_sub = (base_freight + fixed_fee + percentage_cost + distance_cost)
    freight_total = freight_sub * urgency_multiplier

    return {
        'weight_total': weight_total,
        'volume_total': volume_total,
        'weight_cost': w_cost,
        'volume_cost': v_cost,
        'base_freight': base_freight,
        'fixed_fee': fixed_fee,
        'percentage_cost': percentage_cost,
        'distance_cost': distance_cost,
        'urgency_multiplier': urgency_multiplier,
        'urgency_label': urgency.label if urgency else 'Normal',
        'freight_total': freight_total,
    }
