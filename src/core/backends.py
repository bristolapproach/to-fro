from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Based on https://stackoverflow.com/a/37332393


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(
                Q(email=username) | Q(username=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
