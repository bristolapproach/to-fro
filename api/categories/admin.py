from django import forms
from django.contrib import admin
from .models import Ward, HelpType

from django.utils.translation import gettext as _
from markup_help.templatetags.svg import fontawesome_icon_exists

import logging
logger = logging.getLogger(__name__)

admin.site.register(Ward)


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


class HelpTypeAdmin(admin.ModelAdmin):
    form = HelpTypeForm


admin.site.register(HelpType, HelpTypeAdmin)
