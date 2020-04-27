from django import template
from django.utils.safestring import mark_safe
import markdown as md
register = template.Library()


@register.filter()
def markdown(value):
    return mark_safe(md.markdown(value))
