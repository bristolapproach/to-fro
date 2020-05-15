from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
import os
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sets the current django.contrib.site.Site domain
    according to the environment variables
    """

    def handle(self, *args, **options):
        site_url = os.getenv("SITE_URL", "http://0.0.0.0:80")
        domain = site_url.split('://')[-1]
        site = Site.objects.first()
        if not site:
            # The site
            site = Site()
        site.domain = domain
        site.save()
        logger.info('Site domain successfully set to %s', domain)
