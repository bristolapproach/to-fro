from core.notifications import NotificationManager, EmailSender
from core.models import Job, Notification
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from datetime import datetime

# Triggered after saving a Job instance.
# @receiver(post_save, sender=Job)
@receiver(m2m_changed, sender=Job)
def save_job(sender, instance, **kwargs):

    print("Save signal received for Job", instance.id)
    print("Job priority", instance.job_priority.name)
    print("Job status", instance.job_status.name)

    # If it's high priority, send an email immediately.
    if instance.job_priority.name == "high" \
    and instance.job_status.name == "pending_help":
        print("Send email")
        NotificationManager.send_job_email(instance)
    
    
# Triggered after saving a Notification instance.
@receiver(post_save, sender=Notification)
def save_notification(sender, instance, **kwargs):
    print("Signal received for Notification save")
    print("Instance delivered", instance.delivered)
    if not instance.delivered:
        EmailSender.send(instance.subject, instance.message, instance.recipients)
