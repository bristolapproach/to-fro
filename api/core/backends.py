from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailBackend(ModelBackend):
    """Custom email auth backend.
    Based on https://stackoverflow.com/a/37332393
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Use `__iexact` for the email lookup as emails are case insensitive by nature
            # and there might be emails in varying capitalisation in the DB
            # from prior to the fix lowecasing all emails
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
