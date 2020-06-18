from users.models import Coordinator, Resident, Volunteer
from categories.models import HelpType, Ward
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext as _
from django.db.models import Q, IntegerField, Case, When, Value
from core.admin import ModelAdminWithExtraContext
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

import logging
logger = logging.getLogger(__name__)


class UserProfileForm(forms.ModelForm):
    def clean(self):
        super().clean()
        if (not self.cleaned_data.get('user_without_account')):
            if (not self.cleaned_data.get('user')):
                # Check that there is an email set
                email = self.cleaned_data.get('email')
                if (not email):
                    raise forms.ValidationError(
                        _("You need an email to create an account"),
                        code='needs-email'
                    )
                # Check that the email does not already exist
                try:
                    user = User.objects.filter(email=email).get()
                    raise forms.ValidationError(
                        _("An account already exists for %(email)s. Please select the matching account in the list of users."),
                        code='email-exists',
                        params={'email': email}
                    )
                except User.DoesNotExist:
                    return self.cleaned_data


class CoordinatorForm(UserProfileForm):
    class Meta:
        model = Coordinator
        fields = '__all__'


class CoordinatorAdmin(ModelAdminWithExtraContext):
    form = CoordinatorForm

    def extra_context(self, object_id=None):
        return {
            'js_data': {
                'profile_type': 'coordinator',
                'profile_id': object_id
            }
        }

    autocomplete_fields = ['user']

    # Displayed on the admin site in a grid when looking at Users.
    list_display = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('first_name', 'last_name', 'phone', 'email')

    # Fields displayed when editing a User.
    fieldsets = (
        ('Personal details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'phone_secondary', )
        }),
        ('Authentication', {
            'fields': ('user', 'user_without_account')
        }),
        (None, {
            'fields': ('notes',)
        })
    )

    # Search settings.
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    ordering = ('last_name', 'email')


class ResidentAdmin(admin.ModelAdmin):
    model = Resident
    list_display = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ['first_name', 'last_name']

    fieldsets = (
        ('Personal details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'phone_secondary', )
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'address_line_3', 'postcode', 'ward')
        }),
        ('Status', {
            'fields': ('shielded', 'internet_access', 'smart_device', 'confident_online_shopping', 'confident_online_comms')
        }),
        (None, {
            'fields': ('notes',)
        }))


class VolunteerForm(UserProfileForm):
    class Meta:
        model = Volunteer
        fields = '__all__'


class VolunteerAutocompleteJsonView(AutocompleteJsonView):
    """
    Custom AutocompleteJsonView for the Volunteer admin
    to highlight when the Volunteer is interested in an action
    or has helped the resident already
    """

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        for volunteer in data['object_list']:
            prefix = "✋ " if getattr(volunteer, 'interested', False) else ""
            suffix = " ⭐️" if getattr(volunteer, 'has_helped', False) else ""
            volunteer.label = f"{prefix}{volunteer.full_name}{suffix}"
        return data


class VolunteerAdminAutocomplete(admin.ModelAdmin):
    """
    Mixin wrapping the customisations of the autocomplete
    for the Volunteer admin
    """

    def autocomplete_view(self, request):
        # Return our custom autocomplete view
        return VolunteerAutocompleteJsonView.as_view(model_admin=self)(request)

    def get_search_results(self, request, queryset, search_term):
        # Update the search results thanks to the extra query param
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        action_id = request.GET.get('with_interest_for')
        queryset = self.sort_search_results(queryset, action_id)
        return (queryset, use_distinct)

    def sort_search_results(self, queryset, action_id):
        """
        Updates the queryset with some extra information and sorting
        regarding whether the volunteer helped the resident already
        and is interested in the action
        """
        if (action_id):
            # Grab a list of the IDs of interested volunteers
            # and voluteers that helped the resitent already
            # to simplify the upcoming query.
            interested_volunteer_ids = Volunteer.objects.filter(
                actions_interested_in__id=action_id).values_list('id', flat=True)
            volunteers_who_helped_resident_ids = Volunteer.objects.filter(
                action__resident__action__id=action_id
            ).distinct().values_list('id', flat=True)

            # Add a couple of extra information to the query
            # and sort according to them to get volunteers:
            #
            # - interested and that helped
            # - interested
            # - that helped
            # - other
            return queryset.annotate(
                interested=Case(
                    When(id__in=interested_volunteer_ids, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()),
                has_helped=Case(
                    When(id__in=volunteers_who_helped_resident_ids, then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField()
                )
            ).order_by('-interested', '-has_helped')
        return queryset


class VolunteerAdmin(VolunteerAdminAutocomplete, ModelAdminWithExtraContext):
    form = VolunteerForm

    def extra_context(self, object_id=None): return {
        'js_data': {
            'profile_type': 'volunteer',
            'profile_id': object_id
        }
    }

    autocomplete_fields = ['user']

    list_display = ('first_name', 'last_name', 'phone', 'email')
    list_filter = ('first_name', 'last_name', 'phone', 'email')
    search_fields = ['first_name', 'last_name']
    filter_horizontal = ('wards', 'help_types', 'requirements')

    fieldsets = (
        ('Personal details', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'phone_secondary', )
        }),
        ('Authentication', {
            'fields': ('user', 'user_without_account')
        }),
        ('External Links', {
            'fields': ('external_volunteer_id',)
        }),
        ('Volunteering preferences', {
            'fields': ('wards', 'help_types')
        }),
        ('Checks', {
            'fields': (
                'requirements',
            )
        }),
        ('Availability', {
            'fields': ('available_mon_morning', 'available_mon_afternoon', 'available_mon_evening', 'available_tues_morning', 'available_tues_afternoon', 'available_tues_evening', 'available_wed_morning', 'available_wed_afternoon', 'available_wed_evening', 'available_thur_morning', 'available_thur_afternoon', 'available_thur_evening', 'available_fri_morning', 'available_fri_afternoon', 'available_fri_evening', 'available_sat_morning', 'available_sat_afternoon', 'available_sat_evening', 'available_sun_morning', 'available_sun_afternoon', 'available_sun_evening')
        })
    )


class ToFroUserAdmin(UserAdmin):
    """
    Customization of the user admin to allow filtering of the autocomplete
    so it returns only Users that don't already have a profile
    """
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Access', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        profile_type = request.GET.get('without_profile_type')
        profile_id = request.GET.get('profile_id', None)
        queryset = self.filter_search_results(
            queryset, profile_type, profile_id)

        return (queryset, use_distinct)

    def filter_search_results(self, queryset, profile_type, profile_id):
        """
        Filters the search results further to ignore users that already
        have the given profile_type, unless they have the given profile_id
        """
        if (profile_type):
            # Whatever happens only grab the users that have the given
            # profile
            criteria = Q(**{f'{profile_type}__isnull': True})
            if (profile_id):
                # But if we have an ID, make sure it's in the list too
                criteria = criteria | Q(**{profile_type: profile_id})

            return queryset.filter(criteria)

        return queryset


admin.site.register(Resident, ResidentAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.unregister(User)
admin.site.register(User, ToFroUserAdmin)
