from notifications.models import Notification
from notifications import notifications
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from actions.models import Action
import logging
import os


site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, dispatch_uid="UserSave")
def post_save_user(sender, instance, created, **kwargs):
    if created:
        # Send an email invite if the User has just been created.
        notifications.send_invite(instance)


@receiver(post_save, sender=Action, dispatch_uid="ActionSave")
def post_save_action(sender, instance, **kwargs):
    notifications.send_action_mail(instance)


@receiver(post_save, sender=Notification, dispatch_uid="NotificationSave")
def post_save_notification(sender, instance, **kwargs):
    notifications.on_notification_save(instance)
