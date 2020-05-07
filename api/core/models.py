from users.models import Coordinator, Requester, Volunteer, HelpType
from django.contrib.auth import get_user_model
from django.db import models


# Load our custom User model through Django.
User = get_user_model()


# class EventType(models.Model):
#     name = models.CharField(max_length=50, null=True)
#     def __str__(self):
#         return f"{self.name}"


# class Event(models.Model):
#     user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, help_text="Who triggered the event?")
#     event_type = models.ForeignKey(EventType, null=True, on_delete=models.PROTECT, help_text="What was the event?")
#     datetime = models.DateTimeField(null=True, help_text="When was the event?")
#     def __str__(self):
#         return f"{self.id}"

class JobPriority:
    LOW, MEDIUM, HIGH = '1', '2', '3'
    PRIORITIES = [
        (LOW,    'low'),
        (MEDIUM, 'medium'),
        (HIGH,   'high')
    ]


class JobStatus:
    PENDING, INTEREST, ASSIGNED, COMPLETED, \
        COULDNT_COMPLETE = '1', '2', '3', '4', '5'
    STATUSES = [
        (PENDING, 'Pending volunteer interest'),
        (INTEREST, 'Volunteer interest'),
        (ASSIGNED, 'Volunteer assigned'),
        (COMPLETED, 'Completed'),
        (COULDNT_COMPLETE, 'Couldn\'t complete'),
    ]


class Job(models.Model):
    added_by = models.ForeignKey(Coordinator, related_name='added_by', on_delete=models.PROTECT, help_text="What's your name?")
    coordinator = models.ForeignKey(Coordinator, related_name='coordinator', on_delete=models.PROTECT, help_text="Who will mediate this task?")
    call_datetime = models.DateTimeField(null=True, help_text="What time did you receive the call about this task?")
    call_duration = models.DurationField(null=True, blank=True, help_text="How long was the call?")
    requester = models.ForeignKey(Requester, on_delete=models.PROTECT, null=True, help_text="Who made the request?")
    requested_datetime = models.DateTimeField(null=True, help_text="When should the task be completed by?")
    volunteer = models.ForeignKey(Volunteer, on_delete=models.PROTECT, null=True, blank=True, help_text="Who will complete the task?")
    job_status = models.CharField(max_length=1, choices=JobStatus.STATUSES, default=JobStatus.PENDING, help_text="What's the status of this task?")
    job_priority = models.CharField(max_length=1, choices=JobPriority.PRIORITIES, default=JobPriority.LOW, help_text="What priority should this task be given?")
    time_taken = models.DurationField(null=True, help_text="How long did it take to complete the task?", blank=True)
    notes = models.TextField(max_length=500, null=True, blank=True, help_text="Notes from the volunteer.")
    public_description = models.TextField(max_length=500, null=True, blank=True, help_text="Text that gets displayed to volunteers who are browsing tasks.")
    private_description = models.TextField(null=True, blank=True, help_text="Text that only gets displayed to a volunteer when they're assigned to the task.")
    help_type = models.ForeignKey(HelpType, on_delete=models.PROTECT, null=True, help_text="Which kind of help is needed")

    @property
    def ward(self):
        return self.requester.ward

    @property
    def description(self):
        return f"Help with {self.help_type} around {self.ward}"

    @property
    def description_with_date(self):
        return f"{self.description} by {self.requested_datetime.strftime('%d %b')}"

    @property
    def is_pending(self):
        return self.job_status == JobStatus.PENDING

    @property
    def has_interest(self):
        return self.job_status == JobStatus.INTEREST

    @property
    def is_assigned(self):
        return self.job_status == JobStatus.ASSIGNED

    @property
    def can_reveal_private_information(self):
        return self.job_status != JobStatus.PENDING and job_status != JobStatus.INTEREST

    def __str__(self):
        return f"Job: {self.id}"


class Notification(models.Model):
    job = models.ForeignKey(Job, null=True, on_delete=models.PROTECT, help_text="The job the notification is about.")
    subject = models.CharField(max_length=100, null=True, help_text="The notification subject.")
    message = models.TextField(max_length=1000, null=True, help_text="What's your name?")
    delivered = models.BooleanField(default=False, help_text="This field is updated automatically.")
    sent_by = models.CharField(max_length=50, help_text="Who's sending the notification?")
    recipients = models.ManyToManyField(User, related_name='notificationrecipient', default=list, help_text="This field is updated automatically.")
    created_date_time = models.DateTimeField(null=True, help_text="This field is updated automatically.")
    delivered_date_time = models.DateTimeField(null=True, help_text="This field is updated automatically.")
