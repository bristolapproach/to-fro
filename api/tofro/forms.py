from django.forms import BooleanField
from django.contrib.auth.forms import SetPasswordForm

from django.utils import timezone


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
