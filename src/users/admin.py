from users.models import Coordinator, Resident, Volunteer, HelpType, Ward
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.translation import gettext as _
from django.db.models import Q


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


class ModelAdminWithExtraContext(admin.ModelAdmin):
    """
    Base class for creating an admin that automatically adds some
    extra context to the add and change views
    """
    extra_context = {}

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context(request))
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context(object_id=object_id))
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class CoordinatorAdmin(ModelAdminWithExtraContext):
    form = CoordinatorForm

    def extra_context(self, object_id=None): return {
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
        ('Account Details', {
            'fields': ('first_name', 'last_name')
        }),
        ('Authentication', {
            'fields': ('user', 'user_without_account')
        }),
        ('Contact Details', {
            'fields': ('phone', 'phone_secondary', 'email', 'email_secondary')
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
        (None, {
            'fields': ('first_name', 'last_name')
        }),
        ('Contact Details', {
            'fields': ('phone', 'phone_secondary', 'email', 'email_secondary')
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


class VolunteerAdmin(ModelAdminWithExtraContext):
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

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name')
        }),
        ('Authentication', {
            'fields': ('user', 'user_without_account')
        }),
        ('Contact Details', {
            'fields': ('phone', 'phone_secondary', 'email', 'email_secondary')
        }),
        ('Volunteering preferences', {
            'fields': ('wards', 'help_types')
        }),
        ('Availability', {
            'fields': ('available_mon_morning', 'available_mon_afternoon', 'available_mon_evening', 'available_tues_morning', 'available_tues_afternoon', 'available_tues_evening', 'available_wed_morning', 'available_wed_afternoon', 'available_wed_evening', 'available_thur_morning', 'available_thur_afternoon', 'available_thur_evening', 'available_fri_morning', 'available_fri_afternoon', 'available_fri_evening', 'available_sat_morning', 'available_sat_afternoon', 'available_sat_evening', 'available_sun_morning', 'available_sun_afternoon', 'available_sun_evening')
        }),
        ('Checks', {
            'fields': (
                'dbs_number', 'access_to_car', 'driving_license', 'ts_and_cs_confirmed', 'health_checklist_received', 'key_worker', 'id_received'
            )
        })
    )


class ToFroUserAdmin(UserAdmin):
    """
    Customization of the user admin to allow filtering of the autocomplete
    so it returns only Users that don't already have a profile
    """

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        profile_type = request.GET.get('without_profile_type')
        profile_id = request.GET.get('profile_id')
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


admin.site.register(Ward)
admin.site.register(HelpType)
admin.site.register(Resident, ResidentAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)
admin.site.unregister(User)
admin.site.register(User, ToFroUserAdmin)
