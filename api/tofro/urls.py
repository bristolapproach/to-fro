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
from rest_framework.schemas import get_schema_view
from rest_framework import routers
from rest_framework.documentation import include_docs_urls


from tofro.views import LoginView, LogoutView, PasswordResetConfirmView, homepage, resolve_static_path_view
from tofro.lib import login_required
from users.views import UserSettingsView
from actions.views import ActionViewSet, ReferralViewSet, OrganisationViewSet
from users.views import VolunteerViewSet, CoordinatorViewSet, ResidentViewSet
from categories.views import HelpTypeViewSet, RequirementViewSet, WardViewSet, ReferralTypeViewSet

router2 = routers.SimpleRouter()
router2.register(r'actions', ActionViewSet)
router2.register(r'referrals', ReferralViewSet)
router2.register(r'organisations', OrganisationViewSet)
router2.register(r'volunteers', VolunteerViewSet)
router2.register(r'coordinators', CoordinatorViewSet)
router2.register(r'residents', ResidentViewSet)
router2.register(r'helptypes', HelpTypeViewSet)
router2.register(r'referraltypes', ReferralTypeViewSet)
router2.register(r'requirements', RequirementViewSet)
router2.register(r'wards', WardViewSet)

urlpatterns = [
    path('', homepage, name="home"),
    re_path(r'static-path/(?P<path>.+)', resolve_static_path_view),
    path('admin/', admin.site.urls, name="admin"),
    # Take over the password reset confirmation with our own view
    path('accounts/reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include((router2.urls, 'app_name'))),
    path('accounts/', include('django.contrib.auth.urls')),
    path('actions/', decorator_include(login_required, ('actions.urls', 'actions'))),
    path('accounts/login', LoginView.as_view(), name="login"),
    path('accounts/logout', LogoutView.as_view(), name="logout"),
    path('accounts/settings', UserSettingsView.as_view(), name='user-settings'),
    path('notifications/', include('notifications.urls')),
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        #permission_classes='IsAdminUser',
        version="1.0.0",
        url='/',
    ), name='openapi-schema'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    re_path(r'^(?P<url>.*/)$', flatpage, name="page"),
]


# Add the debug toolbar.
if 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns

# Add Redis URLs.
urlpatterns += [
    path('django-rq/', include('django_rq.urls'))
]
