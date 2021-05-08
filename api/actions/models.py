from categories.models import HelpType, Requirement
from users import models as user_models
from django.db import models, transaction
from django.utils import timezone
from model_utils import FieldTracker
import uuid

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
    PENDING, INTEREST, ASSIGNED, ONGOING, COMPLETED, \
        COULDNT_COMPLETE, NO_LONGER_NEEDED = '1', '2', '3', '4', '5', '6', '7'
    STATUSES = [
        (PENDING, 'Pending volunteer interest'),
        (INTEREST, 'Volunteer interest'),
        (ASSIGNED, 'Volunteer assigned'),
        (ONGOING, 'Ongoing'),
        (COMPLETED, 'Completed'),
        (COULDNT_COMPLETE, 'Couldn\'t complete'),
        (NO_LONGER_NEEDED, 'No longer needed')
    ]


class Action(models.Model):

    STATUSES_WITHOUT_ASSIGNED_VOLUNTEER = (
        ActionStatus.INTEREST, ActionStatus.PENDING)

    external_action_id = models.CharField(
        max_length=50, null=True, blank=True, help_text="The ID of the action in an external system")
    added_by = models.ForeignKey(user_models.Coordinator, related_name='added_by',
                                 on_delete=models.PROTECT, help_text="What's your name?")
    coordinator = models.ForeignKey(user_models.Coordinator, related_name='coordinator',
                                    on_delete=models.PROTECT, help_text="Who will mediate this action?")
    call_datetime = models.DateTimeField(
        null=True, help_text="What time did you receive the call about this action?")
    call_duration = models.DurationField(
        null=True, blank=True, help_text="How long was the call?")
    resident = models.ForeignKey(
        user_models.Resident, on_delete=models.PROTECT, null=True, help_text="Who made the request?")
    requested_datetime = models.DateTimeField(
        null=True, verbose_name="Due", help_text="When should the action be completed by?")

    interested_volunteers = models.ManyToManyField(user_models.Volunteer, blank=True, related_name="actions_interested_in",
                                                   help_text="Volunteers who have expressed interest in completing the action..")
    assigned_volunteer = models.ForeignKey(user_models.Volunteer, on_delete=models.PROTECT,
                                           null=True, blank=True, help_text="The volunteer who will complete the action.")
    # LAST FIX assigned_volunteer
    assigned_volunteers = models.ManyToManyField(user_models.Volunteer, blank=True, related_name="actions_assigned_to",
                                           help_text="Volunteers who have been assigned to completing the action..")
    action_status = models.CharField(max_length=1, choices=ActionStatus.STATUSES,
                                     default=ActionStatus.PENDING, help_text="What's the status of this action?")
    action_priority = models.CharField(max_length=1, choices=ActionPriority.PRIORITIES,
                                       default=ActionPriority.MEDIUM, help_text="What priority should this action be given?")
    public_description = models.TextField(max_length=500, null=True, blank=True,
                                          help_text="Text that gets displayed to volunteers who are browsing actions.")
    private_description = models.TextField(
        null=True, blank=True, help_text="Text that only gets displayed to a volunteer when they're assigned to the action.")
    help_type = models.ForeignKey(HelpType, on_delete=models.PROTECT, null=True,
                                  verbose_name="Action type", help_text="Which kind of help is needed")
    requirements = models.ManyToManyField(Requirement, blank=True, related_name="actions",
                                          help_text="Only volunteers matching these requirements will see the action.")
    volunteer_made_contact_on = models.DateTimeField(null=True, blank=True)
    assigned_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Assigned on")
    completed_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Completed on")

    action_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)

    time_taken = models.DurationField(null=True, blank=True)

    minimum_volunteers = models.SmallIntegerField(
        default=1, help_text="minimum number of volunteers required for action")
    maximum_volunteers = models.SmallIntegerField(
        default=1, help_text="maximum number of volunteers required for action")

    # Track changes to the model so we can access the previous status
    # when it changes, and update the volunteer accordingly if it swapped
    # to a status that doesn't have a volunteer assigned
    tracker = FieldTracker()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Ensure that the volunteer(s) gets cleared when we move from a status
        # that has assigned volunteer(s) to one that doesn't.
        if (self.tracker.has_changed('action_status')
            and self.action_status in self.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER
                and self.tracker.previous('action_status') not in self.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER
                and self.tracker.previous('action_status') is not None):
            self.assigned_volunteers.clear()

        # Ensures that the status gets set to assigned if we set volunteer(s)
        # and the status was one that doesn't need a volunteer
        # This needs to happen after the clearing of the volunteer
        # when switching to a status without volunteer so there is no
        # volunteer and we don't update the status
        if (self.pk and self.assigned_volunteers.count() and self.action_status in self.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER):
            self.action_status = ActionStatus.ASSIGNED

        # Track the contact date when setting the status
        # to one implying that contact would have happened
        if self.maximum_volunteers > 1 and self.action_status in (ActionStatus.ONGOING, ActionStatus.COMPLETED, ActionStatus.COULDNT_COMPLETE) and not self.volunteer_made_contact_on:
            self.volunteer_made_contact_on = timezone.now()

        # Track other interesting dates
        if (self.action_status not in self.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER and not self.assigned_date):
            self.assigned_date = timezone.now()
        # if (self.action_status in self.STATUSES_WITHOUT_ASSIGNED_VOLUNTEER and self.assigned_date):
        #     self.assigned_date = None

        if (self.action_status == ActionStatus.COMPLETED and not self.completed_date):
            self.completed_date = timezone.now()
        # if (self.action_status != ActionStatus.COMPLETED and self.completed_date):
        #     self.completed_date = None

        # Only for updates as it runs on a related field
        if self.pk is not None:
            # Update the status according to whether there are interested_volunteers or not
            if (self.action_status == ActionStatus.PENDING and self.interested_volunteers.count() > 0):
                self.action_status = ActionStatus.INTEREST
            if (self.action_status == ActionStatus.INTEREST and self.interested_volunteers.count() == 0):
                self.action_status = ActionStatus.PENDING

        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)

        # Needs to happen after the save so the M2M relation can be saved properly
        # when creating an action
        # Without waiting for the end of the transaction, the volunteer
        # doesn't actually gets saved
        transaction.on_commit(self.save_assigned_volunteer, using=using)

    def save_assigned_volunteer(self):
        """
        Ensures the assigned_volunteer is within the list of interested volunteers
        """
        assigned_volunteers = [assigned for assigned in self.assigned_volunteers.all()]
        self.interested_volunteers.add(*assigned_volunteers)

    def register_interest_from(self, volunteer):
        if volunteer not in self.interested_volunteers.all():
            self.interested_volunteers.add(volunteer)
            self.save()

    def withdraw_interest_from(self, volunteer):
        if volunteer in self.interested_volunteers.all():
            self.interested_volunteers.remove(volunteer)
            self.save()

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
    def is_ongoing(self):
        return self.action_status == ActionStatus.ONGOING

    @property
    def has_interest(self):
        return self.action_status == ActionStatus.INTEREST

    @property
    def is_partially_assigned(self):
        return self.assigned_count >= self.minimum_volunteers
    # FIXED assigned_volunteer

    @property
    def is_fully_assigned(self):
        return self.assigned_count >= self.maximum_volunteers

    @property
    def is_completed(self):
        return self.action_status == ActionStatus.COMPLETED

    @property
    def interested_count(self):
        return self.interested_volunteers.count()

    @property
    def assigned_count(self):
        return self.assigned_volunteers.count()

    @property
    def is_failed(self):
        return self.action_status == ActionStatus.COULDNT_COMPLETE

    @property
    def can_reveal_private_information(self):
        return not (
            self.action_status == ActionStatus.INTEREST or self.action_status == ActionStatus.PENDING)

    @property
    def can_give_feedback(self):
        return self.action_status == ActionStatus.ASSIGNED or self.action_status == ActionStatus.ONGOING

    @property
    def potential_volunteers(self):
        return user_models.Volunteer.objects \
            .filter(wards__id=self.ward.id) \
            .filter(help_types__id=self.help_type.id) \
            .all()

    @property
    def potential_volunteer_ids(self):
        return [v.pk for v in self.potential_volunteers]

    @property
    def checkin_required(self):
        if self.volunteer_made_contact_on or self.maximum_volunteers > 1:
            return False
        else:
            return True

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('actions:detail', kwargs={'action_uuid': self.action_uuid})



    def __str__(self):
        if self.resident:
            return f"Action {self.id} - {self.resident.full_name}"
        else:
            return f"Action {self.id} - No resident"


class ActionFeedback(models.Model):
    action = models.ForeignKey(Action, on_delete=models.PROTECT,
                               null=False, help_text="The feedback subject")
    volunteer = models.ForeignKey(user_models.Volunteer, on_delete=models.PROTECT,
                                  null=True, help_text="Who wrote the feedback")
    time_taken = models.DurationField(null=True, blank=True,
                                      help_text="How long did it take to complete the action?")
    notes = models.TextField(max_length=500, null=True, blank=True,
                             help_text="Notes from the volunteer")
    created_date_time = models.DateTimeField(null=True, blank=True,
                                             help_text="This field is updated automatically.")

    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.created_date_time:
            self.created_date_time = timezone.now()
        super().save(force_insert=force_insert, force_update=force_update,
                     using=using, update_fields=update_fields)

    def __str__(self):
        return f"Feedback {self.id} - Action {self.action.id}"


