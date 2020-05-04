from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Custom User model manager.
    The two functions below are required by Django \
    for it to manage our custom User model.
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#django.contrib.auth.models.CustomUserManager
    """

    def create_user(self, username, first_name, last_name, \
                    role, password=None, **extra_fields):
        '''Validation function and initialiser of User objects.'''
        if not username:
            raise ValueError(_('The username must be set'))
        user = self.model(username=username, first_name=first_name, \
                          last_name=last_name, role=role, \
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, \
                         role, password, **extra_fields):
        '''Validation function and initialiser of super Users.'''
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, first_name, last_name, \
                                role, password, **extra_fields)
