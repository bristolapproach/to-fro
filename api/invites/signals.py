from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.contrib.auth.forms import PasswordResetForm

import os
import logging
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User, weak=False, dispatch_uid="UserInvite")
def on_user_saved(sender, instance, created, *args, **kwargs):
    if created:
        send_invite(instance)


site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")


def send_invite(user):
    if user.email:
        form = PasswordResetForm({'email': user.email})
        form.is_valid()  # Needed for the `save()` to work
        form.save(domain_override=site_url.split('://')[-1],
                  email_template_name='registration/invitation_email.txt',
                  subject_template_name='registration/invitation_subject.txt',
                  extra_email_context={'site_url': site_url})
