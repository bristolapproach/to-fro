from notifications.models import Notification
from notifications import notifications
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import transaction
from actions.models import Action
import django_rq
import logging
import os


site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, dispatch_uid="UserSave")
def post_save_user(sender, instance, created, **kwargs):
    """Send an email invite if the User has just been created."""
    if created:
        notifications.send_invite(instance)


@receiver(post_save, sender=Action, dispatch_uid="ActionSave")
def post_save_action(sender, instance, using=None, **kwargs):
    """Create appropriate notifications when an action changes."""

    # Track whether the priority has changed before enqueuing
    # As the instance inside the worker won't have changed
    priority_has_changed = instance.tracker.has_changed('action_priority')

    # Create the notification only after the save of the action
    # is commited, to ensure action will be found to satisfy
    # the foreign key on the notifications table
    transaction.on_commit(
        lambda: django_rq.enqueue(
            notifications.create_action_notifications, instance, priority_has_changed, result_ttl=0
        ), using=using)


@ receiver(post_save, sender=Notification, dispatch_uid="NotificationSave")
def post_save_notification(sender, instance, **kwargs):
    """Send a notification once it is saved."""
    # Determine if we should send an email.
    if len(instance.recipients) > 0 and not instance.delivered:
        django_rq.enqueue(notifications.send, instance, result_ttl=0)
