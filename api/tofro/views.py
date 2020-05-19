
from django.conf import settings
from django.contrib.auth import views
from django.urls import reverse
from django.shortcuts import resolve_url

from actions.views import ActionsListView
from .lib import has_permission

import logging
logger = logging.getLogger(__name__)


class LoginView(views.LoginView):
    """
    Custom LoginView that redirects users after login
    differently depending on whether they're staff (to admin)
    or not (to the homepage).

    It still honors any parameter coming from the URL
    """

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or self.get_redirect_url_for_user(self.request.user) or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url_for_user(self, user):
        if user.is_staff:
            return reverse('admin:index')


def homepage(request):
    """
    Custom hopepage view that'll delegate its rendering to 
    specific views depending if the user is a Volunteer
    """
    if (has_permission(request.user)):
        return ActionsListView.as_view(list_type='mine')(request)
    else:
        return LoginView.as_view()(request)
