from django.core import management

def daily_digest_volunteer():
    management.call_command('send_digest_emails', 'daily')


def weekly_digest_volunteer():
    management.call_command('send_digest_emails', 'weekly')
