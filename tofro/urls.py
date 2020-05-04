"""tofro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin

from decorator_include import decorator_include
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import url
from core import views
from tofro.lib import login_required

urlpatterns = [
    path('tasks/', decorator_include(login_required, ('tasks.urls', 'tasks'))),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.homepage, name="home")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
