from core.models import Job, Notification
from django.contrib import admin


# Register our models with the admin site.
class JobAdmin(admin.ModelAdmin):
    list_filter = ('requester', 'volunteer', 'requested_datetime', 'job_status')
    fieldsets = (
        (None, {
            'fields': ('requester', 'requested_datetime', 'help_type', 'job_priority')
        }),
        ('Description', {
            'fields': ('public_description', 'private_description')
        }),
        ('Help received', {
            'fields': ('job_status', 'volunteer', 'designated_coordinator', 'timeTaken', 'notes')
        }),
        ('Call details', {
            'fields': ('added_by', 'call_datetime', 'call_duration')
        })
    )

admin.site.register(Job, JobAdmin)
admin.site.register(Notification)
