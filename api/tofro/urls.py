"""tofro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from decorator_include import decorator_include
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.flatpages.views import flatpage

from tofro.views import LoginView, LogoutView, PasswordResetConfirmView, homepage, resolve_static_path_view
from tofro.lib import login_required
from users.views import UserSettingsView


urlpatterns = [
    path('', homepage, name="home"),
    re_path(r'static-path/(?P<path>.+)', resolve_static_path_view),
    path('admin/', admin.site.urls, name="admin"),
    # Take over the password reset confirmation with our own view
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('actions/', decorator_include(login_required, ('actions.urls', 'actions'))),
    path('accounts/login', LoginView.as_view(), name="login"),
    path('accounts/logout', LogoutView.as_view(), name="logout"),
    path('accounts/settings', UserSettingsView.as_view(), name='user-settings'),
    path('notifications/', include('notifications.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    re_path(r'^(?P<url>.*/)$', flatpage, name="page"),
]


# Add the debug toolbar.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = urlpatterns + [
        path('__debug__/', include(debug_toolbar.urls))
    ]

# Add Redis URLs.
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]
