from django.db.models.signals import post_save
from core.models import Job, Notification
from core import notifications


# Register function to trigger after saving a Job.
def save_job(sender, instance, **kwargs):
    notifications.on_job_save(instance)
post_save.connect(save_job, Job, weak=False, dispatch_uid="JobSignal")

# Register function to trigger after saving a Notification.
def save_notification(sender, instance, **kwargs):
    notifications.on_notification_save(instance)
post_save.connect(save_notification, Notification, weak=False, dispatch_uid="NotificationSignal")
