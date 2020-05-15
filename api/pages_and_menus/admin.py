from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from sitetree import admin as sitetree_admin, models

import logging
logger = logging.getLogger(__name__)


class TreeAdmin(sitetree_admin.TreeAdmin):
    """
    Reduce options to add/remove menus in the admin
    So that only the main navigation appears and cannot be removed
    """
    readonly_fields = ('title', 'alias')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TreeItemAdmin(sitetree_admin.TreeItemAdmin):
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
