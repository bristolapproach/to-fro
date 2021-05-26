from .models import Action, ActionPriority, ActionStatus, ActionFeedback
from .models import Referral, Organisation
from categories.models import HelpType

# Register our models with the admin site.
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from django.utils import timezone
from django.db import models
from django.db.models.query import EmptyQuerySet
from django import forms
import datetime
from django.utils.translation import gettext_lazy as _
from core.admin import ModelAdminWithDefaultPagination, ModelAdminWithExtraContext
from admin_auto_filters.filters import AutocompleteFilter
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

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


class MadeContactFilter(admin.SimpleListFilter):
    title = 'Made contact'
    parameter_name = 'made_contact'

    def lookups(self, request, model_admin):
        return (
            ('Yes', 'Yes'),
            ('No', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'Yes':
            return queryset.filter(volunteer_made_contact_on__isnull=False)
        elif value == 'No':
            return queryset.filter(volunteer_made_contact_on__isnull=True, action_status__in=(ActionStatus.ONGOING, ActionStatus.ASSIGNED, ActionStatus.COMPLETED, ActionStatus.COULDNT_COMPLETE))
        return queryset


class VolunteerFilter(AutocompleteFilter):
    title = 'Assigned volunteers'
    field_name = 'assigned_volunteers'
    # FIXED assigned_volunteer


class ResidentFilter(AutocompleteFilter):
    title = 'Resident'
    field_name = 'resident'


class CoordinatorFilter(AutocompleteFilter):
    title = 'Coordinator'
    field_name = 'coordinator'


class AssignedVolunteerAutocompleteSelect(AutocompleteSelectMultiple):
    """
    Custom AutocompletSelect widget for the assigned volunteer
    that appends the ID of the action to the AJAX URL
    """

    def __init__(self, existing_widget, model_instance):
        self.rel = existing_widget.rel
        self.admin_site = existing_widget.admin_site
        self.db = existing_widget.db
        self.choices = existing_widget.choices
        self.attrs = existing_widget.attrs
        self.model_instance = model_instance

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs=extra_attrs)
        url = attrs['data-ajax--url']
        if (self.model_instance.pk):
            query_param = f"with_interest_for={self.model_instance.pk}"
            join_char = "&" if "?" in url else "?"
            attrs['data-ajax--url'] = f"{url}{join_char}{query_param}"
        return attrs


class ActionAdminForm(forms.ModelForm):
    """
    Custom form for the Action admin that
    replaces the widget for `assigned_volunteer`
    """

    def __init__(self, *args, **kwargs):
        super(ActionAdminForm, self).__init__(*args, **kwargs)
        # The widget is actually a RelatedFieldWidgetWrapper
        # (the one that provides the add, edit and delete shortcuts)
        # so it's actually its `widget` that holds
        # the original AutocompleteSelect widget
        if 'assigned_volunteers' in self.fields:
        #if True:
            self.fields['assigned_volunteers'].widget.widget = AssignedVolunteerAutocompleteSelect(
                # FIXED assigned_volunteer
                self.fields['assigned_volunteers'].widget.widget,
                # FIXED assigned_volunteer
                self.instance)


    def clean(self):
        super().clean()
        if self.cleaned_data.get('assigned_volunteers', EmptyQuerySet).count()  \
                > self.cleaned_data['maximum_volunteers']:
            raise forms.ValidationError(
                _("You have assigned more than the maximum number of volunteers")
            )

        if (not self.cleaned_data['assigned_volunteers']
                # FIXED assigned_volunteer
                and self.cleaned_data['action_status'] not in Action.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER + (ActionStatus.NO_LONGER_NEEDED,)):
            raise forms.ValidationError(
                _("Please make sure to update the action status when no volunteer is assigned"),
                code='invalid-status-for-unassigning-volunteer'
            )


    class Meta:
        model = Action
        fields = '__all__'


class FeedbackInline(admin.TabularInline):
    model = ActionFeedback
    min_num = 0
    extra = 0


class ActionAdmin(ModelAdminWithDefaultPagination, ModelAdminWithExtraContext):
    form = ActionAdminForm
    list_display = ('id', 'resident', 'help_type',
                    'requested_datetime', 'has_volunteer_made_contact',  'action_status',  'time_taken',
                    )
                    # FIXED assigned_volunteer
    list_filter = (ResidentFilter,
                   VolunteerFilter,
                   CoordinatorFilter,
                   ('requested_datetime', RequestedDatetimeListFilter),
                   ('action_status', ChoiceDropdownFilter),
                   MadeContactFilter,
                   )
    list_editable = ['action_status',                     ]
    # FIXED assigned_volunteer
    autocomplete_fields = ['resident',
                           'assigned_volunteers',
                           ]
    # FIXED assigned_volunteer
    readonly_fields = ['time_taken', 'action_uuid']
    filter_horizontal = ('requirements', 'interested_volunteers')
    inlines = (FeedbackInline,)

    fieldsets = (
        ('Action Details', {
            'fields': ('resident', 'requested_datetime', 'help_type', 'action_priority', 'coordinator',
                       'minimum_volunteers', 'maximum_volunteers', 'action_uuid', 'requirements')
        }),
        ('External Links', {
            'fields': ('external_action_id',)
        }),
        ('Description', {
            'fields': ('public_description', 'private_description')
        }),
        ('Call details', {
            'fields': ('added_by', 'call_datetime', 'call_duration')
        }),
        ('Help received', {
            'fields': ('action_status', 'assigned_volunteers', 'time_taken', 'volunteer_made_contact_on', 'assigned_date', 'completed_date',)
            # FIXED assigned_volunteer
        }),
    )

    # Necessary for multiple autocomplete filters
    # to be set on the admin it seems
    class Media:
        pass

    def has_delete_permission(self, request, obj=None):
        """
        Prevent deletion of actions
        """
        return False

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Customize the form class to provide initial data based on the request
        as there is not opening for it in Django: https://github.com/django/django/blob/0668164b4ac93a5be79f5b87fae83c657124d9ab/django/contrib/admin/options.py#L1572
        """
        formClass = super().get_form(request, obj=obj, change=change, **kwargs)

        class form(formClass):

            def get_initial_for_field(self, field, field_name):
                initial = super().get_initial_for_field(field, field_name)
                return initial if initial else self.get_initial_from_request(field_name)

            def get_initial_from_request(self, field_name):
                if (field_name == 'requested_datetime'):
                    return get_now().replace(hour=18, minute=0, second=0, microsecond=0)
                elif (field_name == 'call_datetime'):
                    return get_now()
                elif (field_name == 'coordinator' or field_name == 'added_by'):
                    if (request.user.is_coordinator):
                        return request.user.coordinator


        return form

    def get_changelist_form(self, request, **kwargs):
        """
        Allows using the custom autocomplete for the changelist too
        """
        return ActionAdminForm

    def extra_context(self, object_id=None):
        # Query the help types only once
        help_types = HelpType.objects.prefetch_related('requirements').all()

        return {
            'js_data': {
                'action_description_templates': self.get_description_templates(help_types),
                'action_requirements_for_help_types': self.get_requirements_for_help_types(help_types)
            }
        }

    def get_requirements_for_help_types(self, help_types):
        """
        Queries and prepares an index of each HelpType requirements
        """
        return dict((help_type.pk, [
            requirement.id for requirement in help_type.requirements.all()
        ]) for help_type in help_types)

    def get_description_templates(self, help_types):
        """
        Queries and prepares an index of each HelpType description templates
        """
        return dict((help_type.pk, {
            'private_description_template': help_type.private_description_template,
            'public_description_template': help_type.public_description_template
        }) for help_type in help_types)

    def has_volunteer_made_contact(self, obj):
        # Only return a value when relevant, to not clutter the admin
        if obj.action_status in (ActionStatus.ONGOING, ActionStatus.ASSIGNED, ActionStatus.COMPLETED, ActionStatus.COULDNT_COMPLETE):
            return bool(obj.volunteer_made_contact_on)

    has_volunteer_made_contact.boolean = True
    has_volunteer_made_contact.short_description = "Contact"


class ActionFeedbackAdmin(ModelAdminWithDefaultPagination, ModelAdminWithExtraContext):
    list_display = ('id', 'action', 'volunteer', 'resident',
                    'time_taken', 'created_date_time')
    list_filter = ('volunteer', 'action', 'created_date_time')

    def resident(self, af):
        return af.action.resident
    resident.short_description = 'Resident'
    resident.admin_order_field = 'action__resident'


class ReferralAdmin(ModelAdminWithDefaultPagination):
    list_display = ('id', 'resident', 'referral_organisation', 'referral_type', 'referral_status',
                    'coordinator', 'added_by', 'completed_date')

class OrganisationAdmin(ModelAdminWithDefaultPagination):
    list_display = ('name', 'address_line_1', 'postcode', 'contact_name', 'email', 'phone_number')

admin.site.register(Referral, ReferralAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(ActionFeedback, ActionFeedbackAdmin)
