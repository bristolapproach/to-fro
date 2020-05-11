from django.db.models.signals import post_save
from actions.models import Action
from .models import Notification
from core import notifications


# Register function to trigger after saving a Action.
def save_action(sender, instance, **kwargs):
    notifications.on_action_save(instance)


post_save.connect(save_action, Action, weak=False, dispatch_uid="ActionSignal")

# Register function to trigger after saving a Notification.


def save_notification(sender, instance, **kwargs):
    notifications.on_notification_save(instance)


post_save.connect(save_notification, Notification,
                  weak=False, dispatch_uid="NotificationSignal")
