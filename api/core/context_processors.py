import os
import logging
from django.conf import settings as django_settings
from django.shortcuts import resolve_url

logger = logging.getLogger(__name__)


def settings(request):
    """
    Add django settings to the templates under the `settings` variable
    """
    return {
        'settings': django_settings
    }


NAMES_OF_URLS_WITH_KITE = (
    'logout',
    'login',
    'password_reset'
)


def show_kites(request):
    """
    Checks if the view should display a kite in the background or not
    """
    matches_urls_with_kites = request.resolver_match.url_name in NAMES_OF_URLS_WITH_KITE
    is_logged_out_homepage = request.resolver_match.url_name == 'home' and not request.user.is_authenticated
    return {
        'show_kites': matches_urls_with_kites or is_logged_out_homepage
    }
