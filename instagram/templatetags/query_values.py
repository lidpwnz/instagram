from django import template

register = template.Library()


@register.simple_tag
def values(queryset, val, flat=True):
    return queryset.values_list(val, flat=flat)
