from django.contrib.auth.forms import PasswordResetForm
from notifications.models import Notification, NotificationTypes
from notifications.utils import gen_subject_and_message
from actions.models import ActionPriority, ActionStatus
from django.core.mail import EmailMessage
from users.models import Volunteer
from django.utils import timezone
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


def create_action_notifications(action):
    """Sends emails related to this action.
    Depending on what notifications have already been sent, 
    and the type of action, appropriate emails will be delivered.
    """
    # New high-priority, pending actions result in an email sent to appropriate volunteers.
    if action.action_priority == ActionPriority.HIGH \
     and action.action_status == ActionStatus.PENDING:
        recipients = action.potential_volunteers
        create(recipients, action=action,
               notification_type=NotificationTypes.PENDING_HIGH_PRIORITY)

    # Action coordinator is notified when a volunteer shows interest in an action.
    elif action.action_status == ActionStatus.INTEREST:
        recipients = (action.coordinator,)
        create(recipients, action=action,
               notification_type=NotificationTypes.VOLUNTEER_INTEREST)

    # Volunteers are notified when they are assigned to an action.
    elif action.action_status == ActionStatus.ASSIGNED:
        recipients = (action.volunteer,)
        create(recipients, action=action,
               notification_type=NotificationTypes.VOLUNTEER_ASSIGNED)

    # Action coordinator is notified when a volunteer completes an action.
    elif action.action_status == ActionStatus.COMPLETED:
        recipients = (action.coordinator,)
        create(recipients, action=action,
               notification_type=NotificationTypes.ACTION_COMPLETED)

    # Coordinators are notified when a volunteer can't complete an action.
    elif action.action_status == ActionStatus.COULDNT_COMPLETE:
        recipients = (action.coordinator,)
        create(recipients, action=action,
               notification_type=NotificationTypes.ACTION_NOT_COMPLETED)


def create(recipients, subject=None, message=None, action=None, notification_type=None):
    """Instantiates notifications.
    Generates a notification subject and message, depending on the notification_type.
    """
    # Find the latest notification for this action.
    notification = Notification.objects.filter(
        action=action).order_by('-created_date_time').first()

    # Always create a notification if there's no action.
    # Create a notification if there hasn't been a notification for this action, 
    # or if the last notification for this action had a different notification_type.
    if not action or not notification or notification.type != notification_type:
        
        # Generate a subject and message based on the notification_type.
        gen_subject, gen_message = gen_subject_and_message(site_url, notification_type, action)

        # Create the notification.
        notification = Notification(
            action=action,
            type=notification_type,
            delivered=False,
            created_date_time=timezone.now(),
            subject=subject or gen_subject,
            message=message or gen_message)
        notification.save()

    # Add the recipients (two step save due to many-to-many field).
    notification.recipients.set(recipients)

    # Save the notification - triggering a signal to send the email.
    notification.save()


def send(notification):
    # Determine if we should send an email.
    if notification.recipients.exists() \
    and notification.recipients.count() > 0 \
    and not notification.delivered:

        # Send the email.
        EmailMessage(
            notification.subject, 
            notification.message,
            bcc=[r.email for r in notification.recipients.all() if r.email],
        ).send()

        # Update the data.
        notification.delivered_date_time = timezone.now()
        notification.delivered = True
        notification.save()
