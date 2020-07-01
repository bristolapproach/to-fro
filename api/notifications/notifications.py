from django.contrib.auth.forms import PasswordResetForm
from notifications.models import Notification, NotificationTypes
from notifications.utils import gen_subject_and_message
from actions.models import ActionPriority, ActionStatus
from django.core.mail import EmailMessage
from django.utils import timezone
import logging
import os


coordinator_email = os.getenv("COORDINATOR_EMAIL", "coordinators@test.com")
from_email = os.getenv("EMAIL_HOST_USER", "test@test.com")
site_name = os.getenv("ADMIN_SITE_TITLE", "TestTitle")
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
                extra_email_context={
                    'recipient': user.first_name,
                    'site_name': site_name,
                    'site_url': site_url
                })


def create_action_notifications(action):
    """Sends emails related to this action.
    Depending on what notifications have already been sent, 
    and the type of action, appropriate emails will be delivered.
    """
    # New, high-priority, pending actions trigger an email to appropriate volunteers.
    if action.action_priority == ActionPriority.HIGH \
    and action.action_status == ActionStatus.PENDING \
    and not notification_exists(action, NotificationTypes.PENDING_HIGH_PRIORITY):
        create([v.email for v in action.potential_volunteers], action=action,
            notification_type=NotificationTypes.PENDING_HIGH_PRIORITY)

    # Action coordinator is notified when a volunteer shows interest in an action.
    elif action.action_status == ActionStatus.INTEREST \
    and not notification_exists(action, NotificationTypes.VOLUNTEER_INTEREST):
        create([coordinator_email], action=action,
            notification_type=NotificationTypes.VOLUNTEER_INTEREST,
            context={"volunteer_name": action.interested_volunteers.first().first_name})


    # Volunteers are notified about whether or not they're assigned to an action.
    elif action.action_status == ActionStatus.ASSIGNED:

        # 1. Let the assigned volunteer know.
        # If this notification hasn't been sent before, or if it was previously
        # sent to someone else, we should send it to the assigned volunteer.
        if not notification_exists(action, NotificationTypes.VOLUNTEER_ASSIGNED) \
        or action.assigned_volunteer.email != get_latest_notification(action,
        NotificationTypes.VOLUNTEER_ASSIGNED).recipients[0]:
            create([action.assigned_volunteer.email], action=action,
                notification_type=NotificationTypes.VOLUNTEER_ASSIGNED)
        
        # 2. Let those not assigned know.
        # Only send a notification to volunteers that have not received this email for this action.
        notifications = get_all_notifications(action, NotificationTypes.VOLUNTEER_NOT_ASSIGNED)
        already_received = set([r for n in notifications for r in n.recipients])
        recipients = [v.email for v in action.interested_volunteers.all() 
            if v.email not in already_received and 
            v.id != action.assigned_volunteer.id]
        
        if len(recipients) > 0:
            create(recipients, action=action, 
                notification_type=NotificationTypes.VOLUNTEER_NOT_ASSIGNED)


    # Action coordinator is notified when a volunteer completes an action.
    elif action.action_status == ActionStatus.COMPLETED \
    and not notification_exists(action, NotificationTypes.ACTION_COMPLETED):
        create([coordinator_email], action=action,
            notification_type=NotificationTypes.ACTION_COMPLETED)


    # Coordinators are notified when a volunteer can't complete an action.
    elif action.action_status == ActionStatus.COULDNT_COMPLETE \
    and not notification_exists(action, NotificationTypes.ACTION_NOT_COMPLETED):
        create([coordinator_email], action=action,
            notification_type=NotificationTypes.ACTION_NOT_COMPLETED)


    # Coordinators are notified when an action is set to ongoing.
    elif action.action_status == ActionStatus.ONGOING and \
    not notification_exists(action, NotificationTypes.ACTION_ONGOING):
        create([coordinator_email], action=action, 
            notification_type=NotificationTypes.ACTION_ONGOING)
    
    if action.volunteer_made_contact_on \
    and not notification_exists(action, NotificationTypes.VOLUNTEER_CONTACT):
        create([coordinator_email], action=action,
            notification_type=NotificationTypes.VOLUNTEER_CONTACT)


def notification_exists(action, notification_type):
    """True if a notification has been sent for
    this Action and NotificationType."""
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


def create(recipients, subject=None, message=None, action=None, 
           notification_type=None, context={}):
    """Instantiates notifications.
    Generates a notification subject and message,
    depending on the notification_type.
    """
    # Pass the action as context to the email templates.
    context["action"] = action

    # Generate a subject and message based on the notification_type.
    gen_subject, gen_message = gen_subject_and_message(
        site_url, notification_type, action, context)

    # Create the notification.
    notification = Notification(
        action=action,
        type=notification_type,
        delivered=False,
        created_date_time=timezone.now(),
        subject=subject or gen_subject,
        message=message or gen_message,
        recipients=recipients)
    notification.save()


def send(notification):
    # Determine if we should send an email.
    if len(notification.recipients) > 0 and not notification.delivered:

        # Send the email.
        send_email(notification.subject, notification.message,
                   notification.recipients)

        # Update the data.
        notification.delivered_date_time = timezone.now()
        notification.delivered = True
        notification.save()


def send_email(subject, message, recipients):
    logger.log(logging.INFO, f"Sending email: {subject}")
    EmailMessage(
        subject, message,
        bcc=recipients
    ).send()
