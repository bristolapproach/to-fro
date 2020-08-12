from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sitetree import admin as sitetree_admin, models
from core.admin import ModelAdminWithDefaultPagination
from django.urls import reverse
from django.contrib.sites.models import Site
from django.contrib.flatpages import admin as flatpages_admin, models


import logging
logger = logging.getLogger(__name__)


class TreeAdmin(ModelAdminWithDefaultPagination, sitetree_admin.TreeAdmin):
    """
    Reduce options to add/remove menus in the admin
    So that only the main navigation appears and cannot be removed
    """
    readonly_fields = ('title', 'alias')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TreeItemAdmin(ModelAdminWithDefaultPagination, sitetree_admin.TreeItemAdmin):
    """
    Reduce fields available when editing TreeItems
    """
    fieldsets = (
        (_('Basic settings'), {
            'fields': ('title', 'url',)
        }),
        (_('Access settings'), {
            'fields': ('access_loggedin', 'access_guest')
        }),
    )


sitetree_admin.override_tree_admin(TreeAdmin)
sitetree_admin.override_item_admin(TreeItemAdmin)


class FlatPageAdmin(ModelAdminWithDefaultPagination, flatpages_admin.FlatPageAdmin):
    """
    Customization of the FlatPageAdmin
    """
    # Reduce the visible fields in the admin
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'registration_required')}),)

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
