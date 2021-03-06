import logging
from django.core.management.base import BaseCommand
from sitetree.models import Tree


logger = logging.getLogger(__name__)

MENUS = (
    ('main_navigation', 'Main navigation'),
    ('footer_navigation', 'Footer navigation')
)


class Command(BaseCommand):
    """
    Sets the credentials of a default admin user
    """

    def handle(self, *args, **options):
        [self.create_menu(*menu) for menu in MENUS]

    def create_menu(self, alias, title):
        sitetree = Tree.objects.filter(alias=alias)
        if sitetree:
            logger.info('Main navigation already present, nothing to do')
        else:
            Tree(title=title, alias=alias).save()
            logger.info('Successfully created main navigation tree')
