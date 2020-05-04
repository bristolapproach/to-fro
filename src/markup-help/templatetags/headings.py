from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter()
def heading_level(value, level=1):
    tag_names = [(f'h{i+1}', heading_tag_name(level + i + 1))
                 for i in range(6)]
    replaced = value
    # Reverse the tag names to iterate from the lowest
    # heading level, ensuring that headings don't get
    # successively replaced
    for original, replacement in reversed(tag_names):
        start = f'<{original}'
        start_replacement = f'<{replacement}'
        end = f'</{original}'
        end_replacement = f'</{replacement}'
        replaced = replaced.replace(
            start, start_replacement).replace(end, end_replacement)
    return mark_safe(replaced)


def heading_tag_name(level):
    return f'h{level}' if level < 7 else 'p'
