from users.models import Coordinator, Resident, Volunteer
from categories.models import HelpType, Requirement
from django.db import models

import logging
logger = logging.getLogger(__name__)


class ActionPriority:
    LOW, MEDIUM, HIGH = '1', '2', '3'
    PRIORITIES = [
        (LOW,    'low'),
        (MEDIUM, 'medium'),
        (HIGH,   'high')
    ]


class ActionStatus:
    PENDING, INTEREST, ASSIGNED, COMPLETED, \
        COULDNT_COMPLETE = '1', '2', '3', '4', '5'
    STATUSES = [
        (PENDING, 'Pending volunteer interest'),
        (INTEREST, 'Volunteer interest'),
        (ASSIGNED, 'Volunteer assigned'),
        (COMPLETED, 'Completed'),
        (COULDNT_COMPLETE, 'Couldn\'t complete'),
    ]


class Action(models.Model):
    added_by = models.ForeignKey(Coordinator, related_name='added_by',
                                 on_delete=models.PROTECT, help_text="What's your name?")
    coordinator = models.ForeignKey(Coordinator, related_name='coordinator',
                                    on_delete=models.PROTECT, help_text="Who will mediate this action?")
    call_datetime = models.DateTimeField(
        null=True, help_text="What time did you receive the call about this action?")
    call_duration = models.DurationField(
        null=True, blank=True, help_text="How long was the call?")
    resident = models.ForeignKey(
        Resident, on_delete=models.PROTECT, null=True, help_text="Who made the request?")
    requested_datetime = models.DateTimeField(
        null=True, help_text="When should the action be completed by?")
    volunteer = models.ForeignKey(Volunteer, on_delete=models.PROTECT,
                                  null=True, blank=True, help_text="Who will complete the action?")
    action_status = models.CharField(max_length=1, choices=ActionStatus.STATUSES,
                                     default=ActionStatus.PENDING, help_text="What's the status of this action?")
    action_priority = models.CharField(max_length=1, choices=ActionPriority.PRIORITIES,
                                       default=ActionPriority.LOW, help_text="What priority should this action be given?")
    time_taken = models.DurationField(
        null=True, help_text="How long did it take to complete the action?", blank=True)
    notes = models.TextField(max_length=500, null=True,
                             blank=True, help_text="Notes from the volunteer.")
    public_description = models.TextField(max_length=500, null=True, blank=True,
                                          help_text="Text that gets displayed to volunteers who are browsing actions.")
    private_description = models.TextField(
        null=True, blank=True, help_text="Text that only gets displayed to a volunteer when they're assigned to the action.")
    help_type = models.ForeignKey(
        HelpType, on_delete=models.PROTECT, null=True, help_text="Which kind of help is needed")
    requirements = models.ManyToManyField(
        Requirement, related_name="actions", help_text="Only volunteers matching these requirements will see the action.")

    @property
    def ward(self):
        return self.resident.ward

    @property
    def description(self):
        return f"Help with {self.help_type} around {self.ward}"

    @property
    def description_with_date(self):
        return f"{self.description} by {self.requested_datetime.strftime('%d %b')}"

    @property
    def is_pending(self):
        return self.action_status == ActionStatus.PENDING

    @property
    def has_interest(self):
        return self.action_status == ActionStatus.INTEREST

    @property
    def is_assigned(self):
        return self.action_status == ActionStatus.ASSIGNED

    @property
    def can_reveal_private_information(self):
        return not (
            self.action_status is ActionStatus.INTEREST or self.action_status is ActionStatus.PENDING)

    def __str__(self):
        return f"Action: {self.id}"
