from django.forms import BooleanField
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm

from django.utils import timezone
import django_rq


class SetFirstPasswordForm(SetPasswordForm):
    """
    A password reset form with an extra checkbox for accepting
    terms and conditions
    """
    accepts_terms_and_conditions = BooleanField(required=True)

    def save(self, commit=True):
        user = super().save(commit)
        user.settings.terms_accepted_at = timezone.now()
        # Handle `commit` just like the overriden method
        if (commit):
            user.settings.save()
        # And don't forget to return the user
        return user


class ToFroPasswordResetForm(PasswordResetForm):
    """
    Override PasswordResetForm so that email can be sent asychronously
    """
    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):

         django_rq.enqueue(PasswordResetForm().send_mail, subject_template_name,
                 email_template_name, context, from_email, to_email,
                 html_email_template_name)

