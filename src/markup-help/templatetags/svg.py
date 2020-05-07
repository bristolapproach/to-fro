from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Embeds the SVG at the given path, adding a width and height attribute
@register.simple_tag()
def embed_svg(path, width=20, height=20, role="presentation", class_attribute=None):
    with open(path, 'r') as content_file:
        content = content_file.read()
    if (class_attribute):
        class_attribute = f' class="{class_attribute}"'
    content = content.replace(
        '<svg', f'<svg role={role} width="{width}" height="{height}" {class_attribute}')
    return mark_safe(content)


@register.simple_tag()
def embed_fontawesome(icon_name, icon_set="solid", fallback=None, **kwargs):
    try:
        return embed_svg(f"node_modules/@fortawesome/fontawesome-free/svgs/{icon_set}/{icon_name}.svg", **kwargs)
    except:
        return embed_fontawesome(icon_name, icon_set, fallback=None, **kwargs)
