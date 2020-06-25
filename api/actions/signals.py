from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ActionFeedback
import datetime


@receiver(post_save, sender=ActionFeedback, dispatch_uid="UpdateVolunteerTime")
def post_save_action_feedback(sender, instance, created, **kwargs):
    # Extracted in a separate function to allow easy reuse
    # if we want to tally on actions or resident
    update_time_total(instance.volunteer)


def update_time_total(volunteer):
    """
    Sums the amount of time the volunteer has provided
    """
    total = datetime.timedelta()
    for action_feedback in volunteer.actionfeedback_set.all():
        total = total + \
            (action_feedback.time_taken or datetime.timedelta())
    volunteer.time_given = total
    volunteer.save()
