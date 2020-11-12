import datetime

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404

from actions.models import ActionPriority
from users.models import Volunteer


def _is_logged_in_admin(user):
    return user.is_superuser and user.is_authenticated


def _get_digest_actions_common(volunteer):

    # all actions available (total, not just recent and regardless of priority)
    available_actions = volunteer.available_actions.order_by(
        'requested_datetime', '-action_priority'
    )

    # "high priority" actions still available (total, not just recent ones)
    hp_available_actions = volunteer.available_actions.filter(
        action_priority=ActionPriority.HIGH
    ).order_by('requested_datetime')

    # actions waiting for approval (this is total and one's they've
    # volunteered for, but no volunteer has been assigned yet)
    actions_awaiting_approval = volunteer.actions_interested_in.filter(
        assigned_volunteer__isnull=True).order_by('requested_datetime')

    # ongoing (total ones they are assigned to and are still ongoing)
    ongoing_actions = volunteer.ongoing_actions.order_by(
        'requested_datetime', '-action_priority'
    )

    # todo: temp
    from actions.models import Action
    all_actions = Action.objects.all()[:5]
    available_actions, actions_awaiting_approval = all_actions, all_actions

    sections = [
        ('Actions available', available_actions),
        ('High-priority actions', hp_available_actions),
        ('Your actions - awaiting approval', actions_awaiting_approval),
        ('Your current actions', ongoing_actions)
    ]
    return sections


@user_passes_test(_is_logged_in_admin)
def daily_digest_volunteer_email_preview(request, volunteer_pk):

    volunteer = get_object_or_404(Volunteer, pk=volunteer_pk)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    twenty_four_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=24)

    sections_common = _get_digest_actions_common(volunteer)

    # actions added in the past 24 hours
    new_available_actions = volunteer.available_actions.order_by(
        'requested_datetime', '-action_priority'
    ).filter(call_datetime__gte=twenty_four_hours_ago)

    # upcoming today (ones they have been approved for and are happening today)
    upcoming_actions_today = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__date=today)

    # upcoming tomorrow (ones they have been approved for and are happening tomorrow)
    upcoming_actions_tomorrow = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__date=tomorrow)

    action_sections = sections_common + [
        ('New actions available', new_available_actions),
        ('Upcoming today', upcoming_actions_today),
        ('Upcoming tomorrow', upcoming_actions_tomorrow),
    ]

    context = {
        'volunteer': volunteer,
        'action_sections': action_sections
    }

    return render(request, 'notifications/action_digest_email.html', context)


@user_passes_test(_is_logged_in_admin)
def weekly_digest_volunteer_email_preview(request, volunteer_pk):

    volunteer = get_object_or_404(Volunteer, pk=volunteer_pk)
    two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)

    sections_common = _get_digest_actions_common(volunteer)

    # x upcoming total (ones they have been approved for that are in the future)
    upcoming_actions = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__gte=two_hours_ago)

    action_sections = sections_common + [
        ('Upcoming actions', upcoming_actions),
    ]

    context = {
        'volunteer': volunteer,
        'action_sections': action_sections
    }
    return render(request, 'notifications/action_digest_email.html', context)
