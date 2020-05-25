import os
import logging
from django.conf import settings as django_settings

logger = logging.getLogger(__name__)


def settings(request):
    """
    Add django settings to the templates under the `settings` variable
    """
    return {
        'settings': django_settings
    }
