import datetime
import os

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from notifications.notifications import send_email
from notifications.views import get_daily_action_sections
from users.models import Volunteer


import logging
logger = logging.getLogger(__name__)


# skip when "no new available today & no available high priority & no upcoming today"
# new_available_actions.count() == 0  (both)
# hp_available_actions.count() == 0  (both)
# upcoming_actions_today.count() == 0  (daily)


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

            self.send_volunteer_daily_digest_email(
                volunteer, action_sections, today, tomorrow,
                'Your daily digest', 'notifications/action_digest_email.html'
            )

    def send_weekly_emails(self, volunteers):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)

        for volunteer in volunteers:
            if not volunteer.email:
                logger.error(f"Volunteer {volunteer.pk} has no email address")
                continue

            action_sections = get_daily_action_sections(volunteer, today, tomorrow)

            # don't send email when these sections are empty
            skip_keys = ['new_available_actions', 'hp_available_actions']
            if all(action_sections[k].count() == 0 for k in skip_keys):
                continue

            self.send_volunteer_daily_digest_email(
                volunteer, action_sections, today, tomorrow,
                'Your weekly digest', 'notifications/weekly_digest_email.html'
            )

    @staticmethod
    def send_digest_email(
        volunteer, action_sections, today, tomorrow,
        subject_title, template_file
    ):
        context = {
            'volunteer': volunteer,
            'action_sections': action_sections,
            'today': today,
            'tomorrow': tomorrow,
            'title': 'Volunteer Daily Digest',
            'request': None
        }
        # todo: hard code as prod url
        os.environ['DJANGO_BASE_URL'] = 'dev.tofro.hostedby.bristolisopen.com'

        html_body = render_to_string(template_file, context)

        print(f"sending email to Volunteer {volunteer.pk}: {volunteer.email}")

        send_email(subject_title, html_body, [volunteer.email])
