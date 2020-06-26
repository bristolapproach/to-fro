from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ActionFeedback
import datetime


@receiver(post_save, sender=ActionFeedback, dispatch_uid="UpdateTimeAfterSave")
@receiver(post_delete, sender=ActionFeedback, dispatch_uid="UpdateTimeAfterDelete")
def post_save_action_feedback(sender, instance, *args, **kwargs):
    # Extracted in a separate function to allow easy reuse
    # if we want to tally on actions or resident
    update_time_total(instance.volunteer, total_attr='time_given',
                      feedback_queryset=instance.volunteer.actionfeedback_set)
    update_time_total(instance.action, total_attr='time_taken',
                      feedback_queryset=instance.action.actionfeedback_set)


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
