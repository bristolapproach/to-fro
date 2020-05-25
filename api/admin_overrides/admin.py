from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

# Set the Django admin site title.
admin.site.site_header = "ToFro Administration"

# Decluter the admin list of apps
admin.site.unregister(Group)
admin.site.unregister(Site)
