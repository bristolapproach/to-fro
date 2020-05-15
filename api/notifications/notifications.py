
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from notifications.models import Notification, NotificationTypes
from actions.models import ActionPriority, ActionStatus
from users.models import Volunteer
import logging
import os


from_email = os.getenv("EMAIL_HOST_USER", "test@test.com")
site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
logger = logging.getLogger(__name__)


def send_invite(user):
    """Sends an email invite to a User instance,
    using Django's PasswordResetForm.
    """
    if user.email:
        form = PasswordResetForm({'email': user.email})
        form.is_valid()  # Needed for the `save()` to work.
        form.save(domain_override=site_url.split('://')[-1],
                email_template_name='registration/invitation_email.txt',
                subject_template_name='registration/invitation_subject.txt',
                extra_email_context={'site_url': site_url})


def send_action_mail(action):
    """Sends emails related to this action.
    Depending on what notifications have already been sent, 
    and the type of action, appropriate emails will be delivered.
    """
    # Check if this is a high-priority, pending action.
    if action.action_priority == ActionPriority.HIGH \
     and action.action_status == ActionStatus.PENDING:
        recipients = action.potential_volunteers
        notify(recipients, action=action,
               notification_type=NotificationTypes.PENDING_HIGH_PRIORITY)

    elif action.action_status == ActionStatus.INTEREST:
        recipients = (action.coordinator,)
        notify(recipients, action=action,
               notification_type=NotificationTypes.VOLUNTEER_INTEREST)

    elif action.action_status == ActionStatus.ASSIGNED:
        recipients = (action.volunteer,)
        notify(recipients, action=action,
               notification_type=NotificationTypes.VOLUNTEER_ASSIGNED)

    elif action.action_status == ActionStatus.COMPLETED:
        recipients = (action.coordinator,)
        notify(recipients, action=action,
               notification_type=NotificationTypes.ACTION_COMPLETED)

    elif action.action_status == ActionStatus.COULDNT_COMPLETE:
        recipients = (action.coordinator,)
        notify(recipients, action=action,
               notification_type=NotificationTypes.ACTION_NOT_COMPLETED)


def notify(recipients, subject=None, message=None, action=None, notification_type=None):
    """
    Creates a notification to the given recipients,
    conputing the
    """

    notification = Notification.objects.filter(
        action=action).order_by('-created_date_time').first()
    if not action or not notification or notification.type != notification_type:
        # Always create a notification if there's no action
        # the action never had a notification or the last notification
        # wasn't of the current type
        rendered_subject_and_message = subject_and_message(
            notification_type, action)

        notification = Notification(
            action=action,
            type=notification_type,
            delivered=False,
            created_date_time=timezone.now(),
            sent_by="Action save signal",
            subject=subject or rendered_subject_and_message['subject'],
            message=message or rendered_subject_and_message['message'])

        notification.save()

    notification.recipients.set(recipients)

    # Save the notification - triggering a signal to send the email.
    notification.save()


def subject_and_message(notification_type, action=None):
    """
    Renders the subject and message for given notification type.
    If an action is provided, the `action_url` and `admin_action_url` will
    also be provided as context to the message template.
    """
    message_context = {} if not action else {
        'action_url': f'{site_url}{reverse("actions:detail", kwargs={"action_id":action.id})}',
        'admin_action_url': f'{site_url}/admin/actions/action/{action.id}/change'
    }
    return {
        # Replace any line breaks in the subject
        # as email header values (like Subject)
        # cannot contain them
        'subject': render_to_string(f'notifications/{notification_type.lower()}_subject.txt') \
        .replace('\n', ' ') \
        .replace('\r', ' '),
        'message': render_to_string(f'notifications/{notification_type.lower()}_message.txt', message_context)
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
