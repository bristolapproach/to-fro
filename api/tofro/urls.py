"""tofro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from decorator_include import decorator_include
from django.urls import include, path
from django.conf.urls.static import static
from django.urls import include, path
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from core import views
from .views import LoginView
from tofro.lib import login_required

urlpatterns = [
    path('', views.homepage, name="home"),
    path('admin/', admin.site.urls, name="admin"),

    path('accounts/', include('django.contrib.auth.urls')),
    path('actions/', decorator_include(login_required, ('actions.urls', 'actions'))),
    path('accounts/login', LoginView.as_view(), name="login"),
    url(r'^password/$', views.change_password, name='change_password')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# Add the debug toolbar.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = urlpatterns + [
        path('__debug__/', include(debug_toolbar.urls))
    ]
