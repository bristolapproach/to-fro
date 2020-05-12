from .models import Action, ActionPriority
from categories.models import HelpType

# Register our models with the admin site.
from django.contrib import admin
from django.utils import timezone
from django.db import models
from django import forms
import datetime
from django.utils.translation import gettext_lazy as _

import logging
logger = logging.getLogger(__name__)


def get_now():
    # Copy a bit of logic from the original DateFieldListFilter
    now = timezone.now()
    # When time zone support is enabled, convert "now" to the user's time
    # zone so Django's definition of "Today" matches what the user expects.
    if timezone.is_aware(now):
        now = timezone.localtime(now)
    return now


class RequestedDatetimeListFilter(admin.DateFieldListFilter):
    """
    Custom filter for requested date time to allow filtering
    future dates rather than past dates
    """

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)

        # Copy a bit of logic from the original DateFieldListFilter
        now = get_now()

        if isinstance(field, models.DateTimeField):
            today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        else:       # field is a models.DateField
            today = now.date()
        tomorrow = today + datetime.timedelta(days=1)
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        next_year = today.replace(year=today.year + 1, month=1, day=1)

        self.links = ((_('Any date'), {}),
                      (_('Past'), {
                          self.lookup_kwarg_until: str(today),
                      }),
                      (_('Today'), {
                          self.lookup_kwarg_since: str(today),
                          self.lookup_kwarg_until: str(tomorrow),
                      }),
                      (_('Tomorrow'), {
                          self.lookup_kwarg_since: str(tomorrow),
                          self.lookup_kwarg_until: str(
                              tomorrow + datetime.timedelta(days=1))
                      }),
                      (_('Within 3 days'), {
                          self.lookup_kwarg_since: str(today),
                          self.lookup_kwarg_until: str(
                              today + datetime.timedelta(days=3))
                      }),
                      (_('Within a week'), {
                          self.lookup_kwarg_since: str(today),
                          self.lookup_kwarg_until: str(
                              today + datetime.timedelta(days=7))
                      })

                      )


class ActionAdmin(admin.ModelAdmin):
    list_display = ('resident', 'help_type',
                    'requested_datetime',  'action_status', 'volunteer')
    list_filter = ('action_status',
                   ('requested_datetime', RequestedDatetimeListFilter),
                   ('resident', admin.RelatedOnlyFieldListFilter),
                   ('volunteer', admin.RelatedOnlyFieldListFilter))
    list_editable = ['action_status', 'volunteer']
    autocomplete_fields = ['resident', 'volunteer']

    fieldsets = (
        ('Action Details', {
            'fields': ('resident', 'requested_datetime', 'help_type', 'action_priority', 'coordinator')
        }),
        ('Description', {
            'fields': ('public_description', 'private_description')
        }),
        ('Help received', {
            'fields': ('action_status', 'volunteer', 'time_taken', 'notes')
        }),
        ('Call details', {
            'fields': ('added_by', 'call_datetime', 'call_duration')
        })
    )

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Customize the form class to provide initial data based on the request
        as there is not opening for it in Django: https://github.com/django/django/blob/0668164b4ac93a5be79f5b87fae83c657124d9ab/django/contrib/admin/options.py#L1572
        """
        formClass = super().get_form(request, obj=obj, change=change, **kwargs)

        class form(formClass):
            def __init__(self, initial={}, **kwargs):
                super().__init__(**{'initial': {
                    **self.get_initial_for_request(request),
                    **initial
                }, **kwargs})

            def get_initial_for_request(self, request):
                initial = {
                    # Prefilled requested datetime to the evening of the day 18:00
                    'requested_datetime': get_now().replace(hour=18, minute=0, second=0, microsecond=0),
                    # Prefilled the call time to now
                    'call_datetime': get_now(),
                    # Set action priority to MEDIUM
                    'action_priority': ActionPriority.MEDIUM
                }
                # Prefill coordinator and added_by to the one corresponding
                # to the current user if applicable
                if request.user.is_coordinator:
                    initial['coordinator'] = request.user.coordinator
                    initial['added_by'] = request.user.coordinator
                return initial

        return form

    def add_view(self, request, form_url='', extra_context=None):
        """
        Custom add view that has the list of action description by help type
        added to the context, ready to be rendered with json_script
        """
        extra_context = extra_context or {}
        extra_context['js_data'] = {
            'action_description_templates': self.get_description_templates()
        }
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Custom add view that has the list of action description by help type
        added to the context, ready to be rendered with json_script
        """
        extra_context = extra_context or {}
        extra_context['js_data'] = {
            'action_description_templates': self.get_description_templates()
        }
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_description_templates(self):
        """
        Queries and prepares an index of each HelpType description templates
        """
        return dict((help_type.pk, {
            'private_description_template': help_type.private_description_template,
            'public_description_template': help_type.public_description_template
        }) for help_type in HelpType.objects.all())


admin.site.register(Action, ActionAdmin)