from collections import namedtuple
import datetime
import logging
import os
from smtplib import SMTPException
import time

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from notifications.views import get_daily_action_sections
from users.models import Volunteer


logger = logging.getLogger(__name__)

RUN_ENV = os.environ.get('RUN_ENV', 'dev')
HOSTNAMES = {  # store this in settings.py?
    'local-dev': 'localhost:8000',
    'dev': 'dev.tofro.hostedby.bristolisopen.com',
    'prod': 'tofro.hostedby.bristolisopen.com'
}
FakeRequest = namedtuple('FakeRequest', ['scheme', 'META'])


class Command(BaseCommand):
    """
    Sends a daily digest of actions to every Volunteer
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'daily_or_weekly', type=str, help='Choose daily or weekly digest'
        )
        parser.add_argument("--volunteer-pk", type=int)

    def handle(self, *args, **options):

        daily_or_weekly = options['daily_or_weekly'].strip().lower()
        volunteer_pk = options['volunteer_pk']

        assert daily_or_weekly in ('daily', 'weekly')

        if volunteer_pk is None:
            volunteers = Volunteer.objects.all()
        else:
            obj = Volunteer.objects.filter(pk=volunteer_pk).first()
            if obj is None:
                print(f"Volunteer {volunteer_pk} not found.")
                exit()
            volunteers = [obj]

        if daily_or_weekly == 'daily':
            self.send_daily_emails(volunteers)
        else:
            self.send_weekly_emails(volunteers)

    def send_daily_emails(self, volunteers):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        for volunteer in volunteers:
            if not volunteer.email:
                logger.error(f"Volunteer {volunteer.pk} has no email address")
                continue

            action_sections = get_daily_action_sections(volunteer, today, tomorrow)

            # don't send email when these sections are empty
            skip_keys = [
                'new_available_actions', 'hp_available_actions',
                'upcoming_actions_today'
            ]
            if all(action_sections[k].count() == 0 for k in skip_keys):
                print(f'skipping {volunteer.pk}')
                continue

            self.send_digest_email(
                volunteer, action_sections, today, tomorrow,
                'Your daily digest', 'notifications/action_digest_email.html'
            )
            time.sleep(2)  # rate-limit to avoid overwhelming email server

    def send_weekly_emails(self, volunteers):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        for volunteer in volunteers:
            if not volunteer.email:
                print(f"Volunteer {volunteer.pk} has no email address")
                continue

            action_sections = get_daily_action_sections(volunteer, today, tomorrow)

            # don't send email when these sections are empty
            skip_keys = ['new_available_actions', 'hp_available_actions']
            if all(action_sections[k].count() == 0 for k in skip_keys):
                print(f'Skipping Volunteer {volunteer.pk}, no actions to display.')
                continue

            self.send_digest_email(
                volunteer, action_sections, today, tomorrow,
                'Your weekly digest', 'notifications/weekly_digest_email.html'
            )
            time.sleep(2)  # rate-limit to avoid overwhelming email server

    @staticmethod
    def send_digest_email(
        volunteer, action_sections, today, tomorrow, subject_title, template_file
    ):
        context = {
            'volunteer': volunteer,
            'action_sections': action_sections,
            'today': today,
            'tomorrow': tomorrow,
            'title': 'Volunteer Daily Digest',
            'request': FakeRequest(
                'https', {'HTTP_HOST': HOSTNAMES[RUN_ENV]}
            ),
            'is_email': True
        }
        html_body = render_to_string(template_file, context)
        email_msg = EmailMessage(
            subject_title, html_body,
            bcc=[volunteer.email],
        )
        email_msg.content_subtype = "html"

        print(f"sending email to Volunteer {volunteer.pk}: {volunteer.email}")
        try:
            email_msg.send(fail_silently=False)
        except SMTPException as e:
            logger.error(f"SMTPException thrown sending email for volunteer {volunteer.pk}: {e}")
