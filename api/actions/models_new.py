from django.db import models, transaction

from categories.models import HelpType, Requirement
from users import models as user_models


OCCURRENCE_TYPES = ['scheduled_in_advance', 'retrospectively_logged']
OCCURRENCE_TYPES = [(s, s) for s in OCCURRENCE_TYPES]

ACTION_PRIORITIES = ['low', 'medium', 'high']
ACTION_PRIORITIES = [(s, s) for s in ACTION_PRIORITIES]

ACTION_OCCURRENCE_STATUSES = ['unassigned', 'assigned_pending', 'complete']
ACTION_OCCURRENCE_STATUSES = [(s, s) for s in ACTION_OCCURRENCE_STATUSES]


class ActionV2(models.Model):

    # fields omitted: added_by, organisation

    external_action_id = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="The ID of the action in an external system"
    )
    resident = models.ForeignKey(
        user_models.Resident, on_delete=models.PROTECT,
        null=True, help_text="Who made the request?"
    )

    coordinator = models.ForeignKey(
        user_models.Coordinator, related_name='coordinator',
        on_delete=models.PROTECT, help_text="Who will mediate this action?"
    )

    action_priority = models.CharField(
        max_length=30, choices=ACTION_PRIORITIES, default='medium',
        help_text="What priority should this action be given?"
    )

    public_description = models.TextField(
        max_length=500, null=True, blank=True,
        help_text="Text that gets displayed to volunteers who are browsing actions."
    )
    private_description = models.TextField(
        null=True, blank=True,
        help_text="Text that only gets displayed to a volunteer when they're assigned to the action."
    )
    help_type = models.ForeignKey(
        HelpType, on_delete=models.PROTECT, null=True,
        verbose_name="Action type", help_text="Which kind of help is needed"
    )
    requirements = models.ManyToManyField(
        Requirement, blank=True, related_name="actions2",
        help_text="Only volunteers matching these requirements will see the action."
    )
    interested_volunteers = models.ManyToManyField(
        user_models.Volunteer
    )
    assigned_volunteers = models.ManyToManyField(
        user_models.Volunteer
    )
    allow_auto_assign = models.BooleanField(default=False)
    allow_auto_assign_on_repetition = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)


class ActionPeriod(models.Model):
    action = models.ForeignKey(ActionV2)

    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    min_volunteers = models.IntegerField(default=1)
    max_volunteers = models.IntegerField(default=1)

    interested_volunteers = models.ManyToManyField(
        user_models.Volunteer
    )
    assigned_volunteers = models.ManyToManyField(
        user_models.Volunteer
    )
    created_datetime = models.DateTimeField(auto_now_add=True)


class ActionOccurrence(models.Model):

    action = models.ForeignKey(ActionV2)
    action_period = models.ForeignKey(ActionPeriod, blank=True, null=True)
    volunteer = models.ForeignKey(user_models.Volunteer, blank=True, null=True)  # null when scheduled_in_advance but nobody assigned yet

    occurrence_type = models.CharField(max_length=50, choices=OCCURRENCE_TYPES)
    status = models.CharField(max_length=80, choices=ACTION_OCCURRENCE_STATUSES)

    due_datetime = models.DateTimeField(blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)


class ActionOccurrenceFeedback(models.Model):
    occurrence = models.ForeignKey(ActionOccurrence)

    time_taken = models.DurationField(null=True, blank=True)
    completed_datetime = models.DateTimeField(null=True, blank=True)

    resident_wants_help_again = models.BooleanField(default=False)
    volunteer_able_to_help_again = models.BooleanField(default=False)
    expected_next_date = models.DateTimeField(blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)

    # notes? (e.g. for coordinator if resident needs help but it's unassigned)
