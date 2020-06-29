
from django.conf import settings
from django.contrib.auth import views
from django.urls import reverse, reverse_lazy
from django.shortcuts import resolve_url
from django.contrib import messages

from actions.views import ActionsListView
from .lib import has_permission
from .forms import SetFirstPasswordForm

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


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    """
    Custom password reset view to display a more welcoming page
    for first resets
    """
    # Save the user some time by logging them in automatically
    post_reset_login = True
    # Redirect them to the homepage
    # reverse_lazy as the URLs are not yet configured
    # when this is called
    success_url = reverse_lazy('home')

    def get_template_names(self):
        if (self.user.password):
            return super().get_template_names()

        return 'registration/password_reset_confirm_invite.html'

    def get_form_class(self):
        if (self.user.password):
            return super().get_form_class()

        return SetFirstPasswordForm

    def form_valid(self, form):
        """
        Builds on the existing form_valid to display a message
        confirming the password has been reset on the page
        the user will be redirected to
        """
        messages.success(self.request, 'Your password was successfully reset!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Adds the user to the request so we can display relevant info
        """
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.user
        })
        return context


def homepage(request):
    """
    Custom hopepage view that'll delegate its rendering to 
    specific views depending if the user is a Volunteer
    """
    if (has_permission(request.user)):
        return ActionsListView.as_view(list_type='mine')(request)
    else:
        return LoginView.as_view()(request)
