import os
import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from actions.models import ActionPriority, ActionStatus
from users.models import Volunteer
from .models import Notification

logger = logging.getLogger(__name__)

site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
from_email = os.getenv("EMAIL_HOST_USER", "test@test.com")


def on_action_save(action):

    # Check if this is a high-priority, pending action.
    if action.action_priority != ActionPriority.HIGH or action.action_status != ActionStatus.PENDING:
        return

    recipients = Volunteer.objects.filter(wards__id=action.ward.id).all()
    notify(recipients, action, **
           subject_and_message(action, 'HIGH_PRIORITY_PENDING'))


def notify(recipients, action, subject=None, message=None):
    notification = Notification.objects.filter(
        action=action).first()
    if not notification:
        notification = Notification(
            action=action,
            delivered=False,
            created_date_time=timezone.now(),
            sent_by="Action save signal",
            subject=subject,
            message=message)

        notification.save()

    notification.recipients.set(recipients)

    # Save the notification - triggering a signal to send the email.
    notification.save()


def subject_and_message(action, notification_type):
    return {
        # Replace any line breaks in the subject
        # as email header values (like Subject)
        # cannot contain them
        'subject': render_to_string(f'notifications/{notification_type.lower()}_subject.txt') \
        .replace('\n', ' ') \
        .replace('\r', ' '),
        'message': render_to_string(f'notifications/{notification_type.lower()}_message.txt', {
            'action_url': f'{site_url}{reverse("actions:detail", kwargs={"action_id":action.id})}'
        })
    }


def on_notification_save(notification):
    # Determine if we should send an email.
    if notification.recipients.exists() \
            and notification.recipients.count() > 0 \
            and not notification.delivered:

        # Send the email.
        send_mail(notification.subject, notification.message, from_email,
                  [r.email for r in notification.recipients.all() if r.email])

        # Update the data.
        notification.delivered_date_time = timezone.now()
        notification.delivered = True
        notification.save()
