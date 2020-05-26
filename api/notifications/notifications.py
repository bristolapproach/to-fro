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
    # New, high-priority, pending actions trigger an email to appropriate volunteers.
    if action.action_priority == ActionPriority.HIGH \
    and action.action_status == ActionStatus.PENDING \
    and not notification_exists(action, NotificationTypes.PENDING_HIGH_PRIORITY):
        create(action.potential_volunteers, action=action,
            notification_type=NotificationTypes.PENDING_HIGH_PRIORITY)


    # Action coordinator is notified when a volunteer shows interest in an action.
    elif action.action_status == ActionStatus.INTEREST \
    and not notification_exists(action, NotificationTypes.VOLUNTEER_INTEREST):
        create([action.coordinator], action=action,
            notification_type=NotificationTypes.VOLUNTEER_INTEREST)


    # Volunteers are notified about whether or not they're assigned to an action.
    elif action.action_status == ActionStatus.ASSIGNED:

        # 1. Let the assigned volunteer know.
        # If this notification hasn't been sent before, or if it was previously
        # sent to someone else, we should send it to the assigned volunteer.
        if not notification_exists(action, NotificationTypes.VOLUNTEER_ASSIGNED) \
        or action.assigned_volunteer.id != get_latest_notification(action,
        NotificationTypes.VOLUNTEER_ASSIGNED).recipients.first().id:
            create([action.assigned_volunteer], action=action,
                notification_type=NotificationTypes.VOLUNTEER_ASSIGNED)
        
        # 2. Let those not assigned know.
        # Only send a notification to volunteers that have not received this email for this action.
        notifications = get_all_notifications(action, NotificationTypes.VOLUNTEER_NOT_ASSIGNED)
        already_received = set([r.id for n in notifications for r in n.recipients.all()])
        recipients = [v for v in action.interested_volunteers.all() 
            if v.id not in already_received and 
            v is not action.assigned_volunteer]
        
        if len(recipients) > 0:
            create(recipients, action=action, 
                notification_type=NotificationTypes.VOLUNTEER_NOT_ASSIGNED)


    # Action coordinator is notified when a volunteer completes an action.
    elif action.action_status == ActionStatus.COMPLETED \
    and not notification_exists(action, NotificationTypes.ACTION_COMPLETED):
        create([action.coordinator], action=action,
            notification_type=NotificationTypes.ACTION_COMPLETED)


    # Coordinators are notified when a volunteer can't complete an action.
    elif action.action_status == ActionStatus.COULDNT_COMPLETE \
    and not notification_exists(action, NotificationTypes.ACTION_NOT_COMPLETED):
        create([action.coordinator], action=action,
            notification_type=NotificationTypes.ACTION_NOT_COMPLETED)
    

def notification_exists(action, notification_type):
    """True if a notification has been sent for this Action and NotificationType."""
    return Notification.objects \
            .filter(action=action) \
            .filter(type=notification_type) \
            .first() is not None

def get_latest_notification(action, notification_type):
    """Returns the latest notification for this Action and NotificationType."""
    return Notification.objects \
            .filter(action=action) \
            .filter(type=notification_type) \
            .order_by('-created_date_time') \
            .first()

def get_all_notifications(action, notification_type):
    """Returns all notifications for this Action and NotificationType."""
    return Notification.objects \
            .filter(action=action) \
            .filter(type=notification_type) \
            .order_by('-created_date_time') \
            .all()


def create(recipients, subject=None, message=None, action=None, notification_type=None):
    """Instantiates notifications.
    Generates a notification subject and message, depending on the notification_type.
    """

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
        send_email(
            notification.subject, notification.message,
            [r.email for r in notification.recipients.all() if r.email])

        # Update the data.
        notification.delivered_date_time = timezone.now()
        notification.delivered = True
        notification.save()

def send_email(subject, message, recipients):
    EmailMessage(
        subject, message,
        bcc=recipients
    ).send()
