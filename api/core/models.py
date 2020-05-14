from django.contrib.auth import get_user_model
from django.db import models
from users.models import Coordinator, Resident, Volunteer, Person
from actions.models import Action


# Load our custom User model through Django.
User = get_user_model()


class Notification(models.Model):
    action = models.ForeignKey(Action, null=True, on_delete=models.PROTECT,
                               help_text="The action the notification is about.")
    subject = models.CharField(
        max_length=100, null=True, help_text="The notification subject.")
    message = models.TextField(
        max_length=1000, null=True, help_text="What's your name?")
    delivered = models.BooleanField(
        default=False, help_text="This field is updated automatically.")
    sent_by = models.CharField(
        max_length=50, help_text="Who's sending the notification?")
    recipients = models.ManyToManyField(
        Person, related_name='notificationrecipient', default=list, help_text="This field is updated automatically.")
    created_date_time = models.DateTimeField(
        null=True, help_text="This field is updated automatically.")
    delivered_date_time = models.DateTimeField(
        null=True, help_text="This field is updated automatically.")
