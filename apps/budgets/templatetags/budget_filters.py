from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

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


@register.filter
def format_payment_info(value):
    """
    Render payment lines with bold titles before ':'
    while keeping values escaped.
    """
    if not value:
        return ''

    lines = str(value).splitlines()
    rendered_lines = []

    for line in lines:
        text = line.strip()
        if not text:
            rendered_lines.append('')
            continue

        if ':' in text:
            title, rest = text.split(':', 1)
            title_html = f"<strong>{escape(title.strip())}:</strong>"
            rest_text = rest.strip()
            if rest_text:
                rendered_lines.append(f"{title_html} {escape(rest_text)}")
            else:
                rendered_lines.append(title_html)
        else:
            rendered_lines.append(escape(text))

    return mark_safe('<br>'.join(rendered_lines))


@register.filter
def to_roman(value):
    """
    Convert a positive integer to its Roman numeral representation.
    Returns '—' for values that cannot be converted.

    E.g.: 1 → I, 4 → IV, 9 → IX, 14 → XIV, 40 → XL, 2024 → MMXXIV
    """
    try:
        n = int(value)
    except (TypeError, ValueError):
        return '—'
    if n <= 0 or n > 3999:
        return str(value)

    val_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100,  'C'), (90,  'XC'), (50,  'L'), (40,  'XL'),
        (10,   'X'), (9,   'IX'), (5,   'V'), (4,   'IV'),
        (1,    'I'),
    ]
    result = ''
    for arabic, roman in val_map:
        while n >= arabic:
            result += roman
            n -= arabic
    return result
