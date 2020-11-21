from collections import namedtuple
import datetime
from email.mime.image import MIMEImage

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from notifications.notifications import send_email
from notifications.views import get_daily_action_sections
from users.models import Volunteer


import logging
logger = logging.getLogger(__name__)

FakeRequest = namedtuple('FakeRequest', ['scheme', 'META'])

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

            self.send_digest_email(
                volunteer, action_sections, today, tomorrow,
                'Your daily digest', 'notifications/action_digest_email.html'
            )

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
                'https', {'HTTP_HOST': 'dev.tofro.hostedby.bristolisopen.com'}
            )
        }

        html_body = render_to_string(template_file, context)

        print(f"sending email to Volunteer {volunteer.pk}: {volunteer.email}")

        # end_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)

        import base64
        images = [
            ('tofro_kites', '/code/static-built/svg/TO_FRO_kites_01-04.svg'),
            ('tofro_logo_knockout', '/code/static-built/img/svg/TO_FRO_logo-04-knockout.svg')
        ]
        images_encoded = {}
        for slug, filepath in images:
            with open(filepath, 'rb') as f:
                images_encoded[slug] = base64.b64encode(f.read())
        context.update(images_encoded)
        
        '''
        images = [
            ('/code/static-built/svg/TO_FRO_kites_01-04.svg', 'svg+xml', 'tofro-kites'),
            ('/code/static-built/img/svg/TO_FRO_logo-04-knockout.svg', 'svg+xml', 'tofro-logo-knockout')
        ]
        attachments = []
        for filepath, subtype, content_id in images:
            with open(filepath, 'rb') as f:
                msgImage = MIMEImage(f.read(), _subtype=subtype)
                msgImage.add_header('Content-ID', content_id)
                attachments.append(msgImage)
        '''

        email_msg = EmailMessage(
            subject_title, html_body,
            bcc=[volunteer.email],
        )
        email_msg.content_subtype = "html"
        email_msg.send()

        #send_email(
        #    subject_title, None, [volunteer.email], html_message=html_body
        #)
