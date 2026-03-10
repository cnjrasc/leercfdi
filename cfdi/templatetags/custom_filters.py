from django import template

register = template.Library()

@register.filter
def custom_format(value):
    try:
        return "{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value

@register.filter
def format_miles_cuatro_decimales(value):
    try:
        return "{:,.4f}".format(value)
    except (ValueError, TypeError):
        return value
    
@register.filter
def format_miles_sin_decimales(value):
    try:
        return "{:,.0f}".format(value)
    except (ValueError, TypeError):
        return value