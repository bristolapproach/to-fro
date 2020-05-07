from django import template

register = template.Library()

THEME_COLOR_MAPPINGS = {
    'error': 'danger',
    'warning': 'warning',
    'success': 'success',
    'info': 'info',
    'debug': 'light'
}

# Maps given state to a boostrap theme color
@register.filter
def boostrap_theme_color(state, prefix=''):
    themeColor = THEME_COLOR_MAPPINGS[state]
    if (prefix):
        return f"{prefix}-{themeColor}"
    else:
        return themeColor
