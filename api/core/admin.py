from .models import Notification
from django.urls import reverse
from django.core import serializers
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.flatpages import admin as flatpages_admin, models


import logging
logger = logging.getLogger(__name__)


class FlatPageAdmin(flatpages_admin.FlatPageAdmin):
    """
    Customization of the FlatPageAdmin
    """

    # Reduce the visible fields in the admin
    fieldsets = ((None, {'fields': ('url', 'title', 'content')}),)

    def save_model(self, request, obj, form, change):
        logger.debug('Change ? %s', change)
        if change:
            # Only saved objects can get items assigned to their
            # Many to many relationships
            obj.sites.set(Site.objects.all())

        super().save_model(request, obj, form, change)

        if not change:
            # Save the related field
            obj.sites.set(Site.objects.all())
            obj.save()

    def view_on_site(self, obj):
        # Fix the view on site for this object
        # As we're on the same site, we can just
        # reverse the URL, making sure we remove the initial slash though
        return reverse('page', kwargs={'url': obj.url[1:]})


admin.site.unregister(models.FlatPage)
admin.site.register(models.FlatPage, FlatPageAdmin)

admin.site.register(Notification)
