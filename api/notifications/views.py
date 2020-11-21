import datetime
from django.db.models import Q
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
    # no longer used?
    # actions_awaiting_approval = volunteer.actions_interested_in.filter(
    #    assigned_volunteer__isnull=True).order_by('requested_datetime')

    # ongoing (total ones they are assigned to and are still ongoing)
    ongoing_actions = volunteer.ongoing_actions.order_by(
        'requested_datetime', '-action_priority'
    )

    '''
    # uncomment when testing templates
    from actions.models import Action
    all_actions = Action.objects.all()[:5]
    available_actions, actions_awaiting_approval = all_actions, all_actions
    ongoing_actions = all_actions
    '''

    sections = {
        'available_actions': available_actions,
        'hp_available_actions': hp_available_actions,
        'ongoing_actions': ongoing_actions
    }
    return sections


def get_daily_action_sections(volunteer, today, tomorrow):

    twenty_four_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=24)

    sections_common = _get_digest_actions_common(volunteer)

    # actions added in the past 24 hours
    new_available_actions = volunteer.available_actions.order_by(
        'requested_datetime', '-action_priority'
    ).filter(call_datetime__gte=twenty_four_hours_ago)

    # high priority that are older than 24 hrs
    old_hp_available_actions = volunteer.available_actions.order_by(
        'requested_datetime', '-action_priority'
    ).filter(~Q(call_datetime__gte=twenty_four_hours_ago), action_priority=ActionPriority.HIGH)

    # upcoming today (ones they have been approved for and are happening today)
    upcoming_actions_today = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__date=today)

    # upcoming tomorrow (ones they have been approved for and are happening tomorrow)
    upcoming_actions_tomorrow = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__date=tomorrow)

    action_sections = {
        'new_available_actions': new_available_actions,
        'upcoming_actions_today': upcoming_actions_today,
        'upcoming_actions_tomorrow': upcoming_actions_tomorrow,
        'old_hp_available_actions': old_hp_available_actions
    }
    action_sections.update(sections_common)

    return action_sections


@user_passes_test(_is_logged_in_admin)
def daily_digest_volunteer_email_preview(request, volunteer_pk):

    volunteer = get_object_or_404(Volunteer, pk=volunteer_pk)

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    action_sections = get_daily_action_sections(volunteer, today, tomorrow)

    context = {
        'volunteer': volunteer,
        'action_sections': action_sections,
        'today': today,
        'tomorrow': tomorrow,
        'title': 'Volunteer Daily Digest',
    }

    import base64
    images = [
        ('tofro_kites', '/code/static-built/img/tofro-kites.png'),
        ('tofro_logo_knockout', '/code/static-built/img/svg/TO_FRO_logo-04-knockout.png')
    ]
    images_encoded = {}
    for slug, filepath in images:
        with open(filepath, 'rb') as f:
            images_encoded[slug] = base64.b64encode(f.read()).decode()
    context.update(images_encoded)

    return render(request, 'notifications/action_digest_email.html', context)


@user_passes_test(_is_logged_in_admin)
def weekly_digest_volunteer_email_preview(request, volunteer_pk):

    volunteer = get_object_or_404(Volunteer, pk=volunteer_pk)
    two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)

    sections_common = _get_digest_actions_common(volunteer)

    # x upcoming total (ones they have been approved for that are in the future)
    upcoming_actions = volunteer.upcoming_actions.order_by(
        '-action_status', 'requested_datetime', '-action_priority'
    ).filter(requested_datetime__gte=two_hours_ago)

    # x upcoming total (ones they have been approved for that are in the future)
    new_available_actions = volunteer.available_actions.order_by(
        'requested_datetime', '-action_priority'
    ).filter(requested_datetime__gte=one_week_ago)

    action_sections = {
        'upcoming_actions': upcoming_actions,
        'new_available_actions': new_available_actions,
    }
    action_sections.update(sections_common)

    context = {
        'volunteer': volunteer,
        'action_sections': action_sections,
        'title': 'Volunteer Weekly Digest',
    }
    return render(request, 'notifications/weekly_digest_email.html', context)
