from users.models import Coordinator, Requester, Volunteer, HelpType, Ward
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _


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


class CoordinatorAdmin(admin.ModelAdmin):
    form = CoordinatorForm

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


class RequesterAdmin(admin.ModelAdmin):
    model = Requester
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


class VolunteerAdmin(admin.ModelAdmin):
    form = VolunteerForm

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


admin.site.register(Ward)
admin.site.register(HelpType)
admin.site.register(Requester, RequesterAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Coordinator, CoordinatorAdmin)