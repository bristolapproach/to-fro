"""tofro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('tasks/', include('tasks.urls')),
    path('', include('polls.urls')),
    path('admin/', admin.site.urls),
]
