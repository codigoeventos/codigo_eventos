from django import template

register = template.Library()


@register.filter
def brl(value):
    """
    Format a number as Brazilian currency notation.
    E.g.: 1234567.89 → 1.234.567,89
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value or ''
    # Python default: "1,234,567.89"
    formatted = f"{value:,.2f}"
    # Convert to Brazilian: "1.234.567,89"
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')


@register.filter
def brl3(value):
    """
    Same as brl but with 3 decimal places.
    E.g.: 1234.5678 → 1.234,568
    """
    try:
        value = float(value)
    except (TypeError, ValueError):
        return value or ''
    formatted = f"{value:,.3f}"
    return formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
