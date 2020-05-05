from core.models import Job, Notification
from django.core import serializers
from users.models import HelpType
from django.contrib import admin
from django.contrib.auth.models import User


# Register our models with the admin site.
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_status', 'requested_datetime',
                    'requester', 'help_type', 'volunteer')
    list_filter = ('job_status', 'requested_datetime',
                   'requester', 'volunteer')
    autocomplete_fields = ['requester', 'volunteer']

    fieldsets = (
        ('Job Details', {
            'fields': ('requester', 'requested_datetime', 'help_type', 'job_priority', 'coordinator')
        }),
        ('Description', {
            'fields': ('public_description', 'private_description')
        }),
        ('Help received', {
            'fields': ('job_status', 'volunteer', 'time_taken', 'notes')
        }),
        ('Call details', {
            'fields': ('added_by', 'call_datetime', 'call_duration')
        })
    )

    def add_view(self, request, form_url='', extra_context=None):
        """
        Custom add view that has the list of job description by help type
        added to the context, ready to be rendered with json_script
        """
        extra_context = extra_context or {}
        extra_context['js_data'] = {
            'job_description_templates': self.get_description_templates()
        }
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Custom add view that has the list of job description by help type
        added to the context, ready to be rendered with json_script
        """
        extra_context = extra_context or {}
        extra_context['js_data'] = {
            'job_description_templates': self.get_description_templates()
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


admin.site.register(Job, JobAdmin)
admin.site.register(Notification)
