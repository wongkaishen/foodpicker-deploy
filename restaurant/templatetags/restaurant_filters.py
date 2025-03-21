from django import template

register = template.Library()

@register.filter
def modulo(value, arg):
    """Returns the remainder of value divided by arg"""
    return int(value) % int(arg)

@register.filter
def animation_delay(value):
    """Returns a CSS class for animation delay based on the value"""
    return f"delay-{int(value) % 10}" 