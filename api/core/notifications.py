from actions.models import Action, ActionPriority, ActionStatus
from users.models import Volunteer
from .models import Notification
from django.core.mail import send_mail
from django.utils import timezone
import os


site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
from_email = os.getenv("EMAIL_HOST_USER", "test@test.com")


def on_action_save(action):
    # Check if this is a high-priority, pending action.
    if action.action_priority != ActionPriority.HIGH or action.action_status != ActionStatus.PENDING:
        return

    # Check for previously created notifications.
    notification = Notification.objects.filter(action__id=action.id).first()
    if notification:

        # We don't want to send the same email twice.
        if not notification.delivered:

            # Update the recipients (perhaps there are more since first created).
            notification.recipients = Volunteer.objects.filter(
                wards__id=action.ward.id).all()

            # Save the notification - triggering a signal to send the email.
            notification.save()
    else:
        # Create the notification in memory.
        notification = Notification(
            action=action,
            delivered=False,
            created_date_time=timezone.now(),
            sent_by="Action save signal",
            subject="High-priority help alert",
            message="Hi!\n\n"
                    "We've received a request for help in your area. \n\n"
                    "Check out the details of the request here:\n"
                    f"{site_url}/actions/{action.id}\n\n"
                    "Thank you!\nThe To-Fro Team")

        # Save the notification to assign the notification an ID.
        # This is required before we can assign recipients due to the Many-to-Many constraint.
        notification.save()

        # Find potential volunteers.
        recipients = Volunteer.objects.filter(wards__id=action.ward.id).all()

        # Assign notification recipients.
        notification.recipients.set(recipients)

        # Save the notification - triggering a signal to send the email.
        notification.save()


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
