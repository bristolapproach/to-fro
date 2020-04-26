"""tofro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls import url
from core import views

urlpatterns = [
    path('tasks/', include('tasks.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^password/$', views.change_password, name='change_password')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)