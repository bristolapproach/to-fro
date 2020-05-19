import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

# Get the admin username and password from the environment.
admin_user = os.getenv("DJANGO_ADMIN_FIRSTNAME", "admin")
admin_password = os.getenv("DJANGO_ADMIN_PASSWORD", "password")


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sets the credentials of a default admin user
    """

    def handle(self, *args, **options):
        # Create the admin user.
        users = User.objects.filter(username=admin_user)
        if users:
            admin = users[0]
            admin.set_password(admin_password)
            admin.save()
            logger.info('Successfully updated admin user credentials')
        else:
            admin = User.objects.create_user(
                username=admin_user, is_staff=True, is_superuser=True)
            admin.set_password(admin_password)
            admin.save()
            logger.info('Successfully created admin user with credentials')
