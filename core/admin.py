from django.contrib import admin
from .models import EventType, Event, Relationship, Ward, Requester, \
    Helper, HelperWard, HelpType, HelpPreference, \
    JobPriority, JobStatus, Job

# Register our models with the admin site.
# admin.site.register(EventType)
# admin.site.register(Event)
admin.site.register(Relationship)
admin.site.register(Ward)
admin.site.register(Requester)


class HelperAdmin(admin.ModelAdmin):
    exclude = ('user_type',)
    fieldsets = (
        (None, {
         'fields': ('first_name', 'last_name')
         }),
        ('Contact details', {
            'fields': ('phone_number_primary', 'phone_number_secondary', 'email_primary', 'email_secondary')
        }),
        ('Volunteering preferences', {
            'fields': ('wards', 'help_types')
        }),
        ('Availability', {
            'fields': ('available_mon_morning', 'available_mon_afternoon', 'available_mon_evening', 'available_tues_morning', 'available_tues_afternoon', 'available_tues_evening', 'available_wed_morning', 'available_wed_afternoon', 'available_wed_evening', 'available_thur_morning', 'available_thur_afternoon', 'available_thur_evening', 'available_fri_morning', 'available_fri_afternoon', 'available_fri_evening', 'available_sat_morning', 'available_sat_afternoon', 'available_sat_evening', 'available_sun_morning', 'available_sun_afternoon', 'available_sun_evening',)
        }),
        ('Checks', {
            'fields': (
                'dbs_number', 'access_to_car', 'driving_license', 'ts_and_cs_confirmed', 'health_checklist_received', 'key_worker', 'id_received'
            )
        })
    )
    pass


admin.site.register(Helper, HelperAdmin)
# admin.site.register(HelperWard)
admin.site.register(HelpType)
admin.site.register(JobPriority)


class JobAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('requester', 'requested_datetime', 'help_type', 'job_priority')
        }),
        ('Description', {
            'fields': ('public_description', 'private_description')
        }),
        ('Help received', {
            'fields': ('job_status', 'helper', 'designated_coordinator', 'timeTaken', 'notes')
        }),
        ('Call details', {
            'fields': ('added_by', 'call_datetime', 'call_duration')
        })
    )
    pass


admin.site.register(Job, JobAdmin)
