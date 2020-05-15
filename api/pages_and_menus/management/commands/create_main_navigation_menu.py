import logging
from django.core.management.base import BaseCommand
from sitetree.models import Tree
import os

# Get the admin username and password from the environment.
admin_user = os.getenv("DJANGO_ADMIN_FIRSTNAME", "admin")
admin_password = os.getenv("DJANGO_ADMIN_PASSWORD", "password")


logger = logging.getLogger(__name__)

MAIN_NAVIGATION_ALIAS = 'main_navigation'


class Command(BaseCommand):
    """
    Sets the credentials of a default admin user
    """

    def handle(self, *args, **options):
        sitetree = Tree.objects.filter(alias=MAIN_NAVIGATION_ALIAS)
        if sitetree:
            logger.info('Main navigation already present, nothing to do')
        else:
            Tree(title="Main navigation", alias=MAIN_NAVIGATION_ALIAS).save()
            logger.info('Successfully created main navigation tree')
