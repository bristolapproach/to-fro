from core.models import Job, Notification, Helper
from django.core.mail import send_mail
import os


site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
from_email = os.getenv("EMAIL_HOST_USER", "test@test.com")

class NotificationManager:

    @staticmethod
    def send_job_email(
        job: Job, subject: str = None, message: str = None, html: bool = False, 
        sent_by: str = None, recipients: list = None):

        # Check for previously created notifications.
        notification = Notification.objects.filter(job__id=job.id).first()
        # We don't want to send the same email twice.
        if notification and not notification.delivered:
            
            # Update the recipients.
            notification.recipients = [hw.helper.email_primary
                for hw in HelperWard.objects.filter(ward=job.ward)
                if hw.helper.email_primary is not None]
            
            # Save the notification - triggering a signal to send the email.
            notification.save()
        else:
            Notification.create(
                subject="High-priority help alert" if job.job_priority.name == "high" else "Help alert",
                message="Hi!\n\n" \
                        "We've received a request for help in your area. \n\n" \
                        "Check out the details of the request here:\n" \
                        f"{site_url}/tasks/{job.id}\n\n" \
                        "Thank you!\nThe To-Fro Team",
                recipients=[hw.helper.email_primary
                    for hw in HelperWard.objects.filter(ward=job.ward)
                    if hw.helper.email_primary is not None])

class EmailSender:

    @staticmethod
    def send(subject, message, recipients):
        print("Sending message to", recipients)
        send_mail(subject, message, from_email, recipients)
