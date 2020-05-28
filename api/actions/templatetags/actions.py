from django import template
register = template.Library()


@register.filter()
def is_awaiting_confirmation_for(action, volunteer):
    return action.has_interest and volunteer in action.interested_volunteers.all()
