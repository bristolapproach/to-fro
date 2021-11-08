from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from .models import ActionFeedback, Action
from django.db import transaction
import django_rq
import datetime

from axes.signals import user_locked_out
from rest_framework.exceptions import PermissionDenied

@receiver(m2m_changed, sender=Action.assigned_volunteers.through, dispatch_uid="AssignedtoInterestedVolunteers")
def post_m2m_action(sender, instance, using=None, action=None, pk_set=[], **kwargs):
    if action == 'post_add':
        assigned = [vol for vol in instance.assigned_volunteers.all()]
        instance.interested_volunteers.add(*assigned)

@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")


@receiver(post_save, sender=ActionFeedback, dispatch_uid="UpdateTimeAfterSave")
@receiver(post_delete, sender=ActionFeedback, dispatch_uid="UpdateTimeAfterDelete")
def post_save_action_feedback(sender, instance, using=None, **kwargs):
    transaction.on_commit(
        lambda: django_rq.enqueue(
            update_totals, instance, result_ttl=0
        ), using=using)


def update_totals(feedback):
    # Extracted in a separate function to allow easy reuse
    # if we want to tally on actions or resident
    update_time_total(feedback.volunteer, total_attr='time_given',
                      feedback_queryset=feedback.volunteer.actionfeedback_set)
    update_time_total(feedback.action, total_attr='time_taken',
                      feedback_queryset=feedback.action.actionfeedback_set)
    update_time_total(feedback.action.resident, total_attr='time_received',
                      feedback_queryset=ActionFeedback.objects.filter(
                          actions_assigned_to__resident=feedback.action.resident))


def update_time_total(instance, total_attr='', feedback_queryset=''):
    """
    Sums the amount of time of the given `feedback_queryset`
    and stores it in the `total_attr` of given `instance`
    """
    total = datetime.timedelta()
    for action_feedback in feedback_queryset.all():
        total = total + \
            (action_feedback.time_taken or datetime.timedelta())
    setattr(instance, total_attr, total)
    instance.save()
