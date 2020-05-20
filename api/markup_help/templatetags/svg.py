from django import template
from django.utils.safestring import mark_safe
import re
import os
import logging
logger = logging.getLogger(__name__)

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


DEFAULT_FONTAWESOME_ICON_SET = "solid"


@register.simple_tag()
def embed_fontawesome(icon_name, icon_set=DEFAULT_FONTAWESOME_ICON_SET, fallback=None, **kwargs):
    try:
        return embed_svg(fontawesome_icon_path(icon_name, icon_set), **kwargs)
    except:
        if fallback:
            return embed_fontawesome(fallback, icon_set=icon_set, fallback=None, **kwargs)
    # Ensures nothing gets printed if fallback fails
    return ''


def fontawesome_icon_path(icon_name, icon_set=DEFAULT_FONTAWESOME_ICON_SET):
    return f"node_modules/@fortawesome/fontawesome-free/svgs/{icon_set}/{icon_name}.svg"


def fontawesome_icon_exists(icon_name, icon_set=DEFAULT_FONTAWESOME_ICON_SET):
    return os.path.isfile(fontawesome_icon_path(icon_name, icon_set))
