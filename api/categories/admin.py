from django import forms
from django.contrib import admin
from .models import Ward, HelpType, Requirement

from core.admin import ModelAdminWithDefaultPagination
from django.utils.translation import gettext as _
from markup_help.templatetags.svg import fontawesome_icon_exists

import logging
logger = logging.getLogger(__name__)

admin.site.register(Ward, ModelAdminWithDefaultPagination)
admin.site.register(Requirement, ModelAdminWithDefaultPagination)


class HelpTypeForm(forms.ModelForm):
    def clean(self):
        super().clean()
        icon_name = self.cleaned_data.get('icon_name')
        if (icon_name):
            if (not fontawesome_icon_exists(icon_name)):
                raise forms.ValidationError(
                    _("FontAwesome does not have an icon named \"%(icon_name)s\"."),
                    code='fontawesome-icon-does-not-exist',
                    params={'icon_name': icon_name}
                )

    class Meta:
        model = HelpType
        fields = '__all__'


class HelpTypeAdmin(ModelAdminWithDefaultPagination):
    form = HelpTypeForm
    fieldsets = (
        (None, {'fields': ('name', 'icon_name')}),
        ('Requirements', {'fields': ('requirements',
                                     'minimum_volunteers',
                                     'maximum_volunteers')}),
        ('Templates', {
         'fields': ('private_description_template', 'public_description_template')})
    )
    filter_horizontal = ('requirements',)


admin.site.register(HelpType, HelpTypeAdmin)
