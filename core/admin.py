from django.contrib import admin
from .models import Action, Event, Relationship, Ward, Requester, \
                    Helper, HelperWard, HelpType, HelpPreference, \
                    JobPriority, JobStatus, Job

# Register our models with the admin site.
admin.site.register(Action)
admin.site.register(Event)
admin.site.register(Relationship)
admin.site.register(Ward)
admin.site.register(Requester)
admin.site.register(Helper)
admin.site.register(HelperWard)
admin.site.register(HelpType)
admin.site.register(HelpPreference)
admin.site.register(JobPriority)
admin.site.register(JobStatus)
admin.site.register(Job)
