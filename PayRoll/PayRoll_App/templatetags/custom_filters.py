from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key, "")

@register.filter
def get_attr_or_key(value, key):
    if value is None:
        return ""
    if hasattr(value, key):
        return getattr(value, key)
    if isinstance(value, dict):
        return value.get(key, "")
    return ""