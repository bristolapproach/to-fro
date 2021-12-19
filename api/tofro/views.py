
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.shortcuts import resolve_url
from whitenoise.middleware import WhiteNoiseMiddleware

from actions.views import ActionsListView, CoordinatorDashboardView
from users.models import volunteer_check, coordinator_check
from .lib import has_permission
from .forms import SetFirstPasswordForm, ToFroPasswordResetForm

import logging
logger = logging.getLogger(__name__)


class LoginRedirection:
    """
    Mixin for sharing the redirections after login
    """

    def get_redirect_url_for_user(self, user):
        """
        Pick where to redirect the user depending on 
        the profiles they have
        """
        if user.is_coordinator:
            return reverse('actions:coordinator_dashboard')
        elif user.is_volunteer:
            return reverse('home')

        return reverse('admin:index')


class LogoutView(views.LogoutView):
    next_page = reverse_lazy('home')

    def get_next_page(self):
        messages.success(self.request, "You're now logged out!")
        return super().get_next_page()


class LoginView(LoginRedirection, views.LoginView):
    """
    Custom LoginView that redirects users after login
    differently depending on whether they're staff (to admin)
    or not (to the homepage).

    It still honors any parameter coming from the URL
    """

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or self.get_redirect_url_for_user(self.request.user) or resolve_url(settings.LOGIN_REDIRECT_URL)


class ToFroPasswordResetView(views.PasswordResetView):
    form_class = ToFroPasswordResetForm



class PasswordResetConfirmView(LoginRedirection, views.PasswordResetConfirmView):
    """
    Custom password reset view to display a more welcoming page
    for first resets
    """
    # Save the user some time by logging them in automatically
    post_reset_login = True
    post_reset_login_backend = 'core.backends.EmailBackend'

    def get_success_url(self):
        return self.get_redirect_url_for_user(self.user)

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

    if request.user.is_authenticated:
        if coordinator_check(request.user):
            return CoordinatorDashboardView.as_view()(request)
        elif volunteer_check(request.user):
            return ActionsListView.as_view(list_type='mine')(request)

    return LoginView.as_view()(request)


def _is_logged_in_admin(user):
    return user.is_superuser and user.is_authenticated


@user_passes_test(_is_logged_in_admin)
def resolve_static_path_view(request, path):
    """
    Resolves a static url path to a concrete filepath.
    For debugging purposes only.
    """
    path = path.rstrip('/')
    middleware = WhiteNoiseMiddleware()
    result = middleware.find_file('/static/' + path)
    if result is None:
        return HttpResponse('File not found')
    filepath = result.alternatives[0][1]
    return HttpResponse(filepath)
