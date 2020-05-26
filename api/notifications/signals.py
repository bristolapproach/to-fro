from notifications.models import Notification
from notifications import notifications
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
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
def post_save_action(sender, instance, created, **kwargs):
    """Create appropriate notifications when an action changes."""
    django_rq.enqueue(notifications.create_action_emails, instance, result_ttl=0)
    if created:
        django_rq.enqueue(notifications.create_action_notifications, instance, result_ttl=0)


@receiver(post_save, sender=Notification, dispatch_uid="NotificationSave")
def post_save_notification(sender, instance, **kwargs):
    """Send a notification once it is saved."""
    # Determine if we should send an email.
    if instance.recipients.exists() \
    and instance.recipients.count() > 0 \
    and not instance.delivered:
        django_rq.enqueue(notifications.send, instance, result_ttl=0)
