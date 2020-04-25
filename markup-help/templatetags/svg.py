from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Embeds the SVG at the given path, adding a width and height attribute
@register.simple_tag()
def embed_svg(path, width= 20, height= 20):
  with open(path, 'r') as content_file:
    content = content_file.read()
  content = content.replace('<svg', f'<svg width="{width}" height="{height}"')
  return mark_safe(content)
    