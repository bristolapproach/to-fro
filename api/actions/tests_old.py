import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from actions.models import (
    ActionV2, ActionOccurrence, ActionOccurrenceVolunteerAssignment,
    ActionOccurrenceVolunteerAssignmentFeedback
)
from categories.models import HelpType, Requirement
from users.models import Volunteer, Resident, Coordinator


HELP_TYPES = [
    'dog_walking', 'prescription_pickup'
]
REQUIREMENTS_BY_HELP_TYPE = {
    'dog_walking': ['dbs_check', 'experience_with_dogs'],
    'prescription_pickup': ['dbs_check']
}

REQUIREMENTS_ALL = set()
for help_type_slug, requirements_slugs in REQUIREMENTS_BY_HELP_TYPE.items():
    REQUIREMENTS_ALL.add(requirements_slugs)
REQUIREMENTS_ALL = [s for s in REQUIREMENTS_ALL]


def create_volunteer(index, help_types, requirements):
    volunteer1_user = User.objects.create_user(
        f'volunteer{index}', f'volunteer{index}@gmail.com',
        f'volunteer{index}-password'
    )
    volunteer = Volunteer.objects.create(
        user=volunteer1_user, first_name='volunteer',
        last_name=str(index),
    )
    if help_types:
        volunteer.help_types.add(*help_types)
    if requirements:
        volunteer.requirements.add(*requirements)
    return volunteer


def create_coordinator(index):
    coordinator1_user = User.objects.create_user(
        f'coordinator{index}', f'coordinator{index}@gmail.com',
        f'coordinator{index}-password'
    )
    coordinator = Coordinator.objects.create(
        user=coordinator1_user, first_name='coordinator',
        last_name=str(index)
    )
    return coordinator


class ActionTestCase(TestCase):

    def setUp(self):

        self.help_types = {
            slug: HelpType(name=slug) for slug in HELP_TYPES
        }
        self.reqs = {}
        for help_type_slug, requirements_slugs in REQUIREMENTS_BY_HELP_TYPE.items():
            for slug in requirements_slugs:
                self.reqs[slug] = Requirement.objects.get_or_create(name=slug)[0]

        self.resident1 = Resident.objects.create(
            first_name='John', last_name='Smith',
            address_line_1='100 Wilton St'
        )

        self.coordinator1 = create_coordinator(1)

        self.volunteer1 = create_volunteer(  # how do they sign up?
            1, self.help_types.values(),
            [self.reqs['dbs_check'], self.reqs['experience_with_dogs']]
        )


    '''
    
    -details
    -periods
    -occurrences
    
    - once-off task e.g. dog walking 
            -> new period (with due_date, chosen)
            -> volunteer contacts resident, agrees on date/time -> calendar event
            -> volunteer gives feedback
                if occurrence exists:
                    occurrence = period.occurrence
                else:
                    create occurrence with retro date
                - save feedback
            
        
            - period closed
            if wants_help_again:
                -  start new period (no due-date, at discresion of volunteer)
                if able_to_help_again:
                    - assign volunteer to new period
                    
                    if volunteer_wants_to_schedule_next_occurrence:
                        pass  # create occurrence
                    else:
                        pass  # 
                else:
                    
                    if next_date: ("do you know when action needs doing next?")
                        pass  # set due-date of new period (so coordinator doesn't have to)
                    else:
                        pass  # nothing happens  (coordinator will see: open periods that are unassigned)
            else:
                # 'close' action
    
    '''

    def dog_walking_initial(self):

        weeks_time = datetime.datetime.now() + datetime.timedelta(days=7)
        now = datetime.datetime.now()

        # 1) coordinator creates dog-walking Action for Resident
        action = ActionV2.objects.create(
            resident=self.resident1, action_priority='medium',
            help_type=self.help_types['dog_walking']
        )
        action.requirements.add(self.reqs['experience_with_dogs'])

        # 2) for dog-walking, coordinator is forced to create an occurrence
        occurrence = ActionOccurrence.objects.create(
            action=action, status='pending', due_datetime=weeks_time
        )

        # 2) volunteer expresses interest in action (with occurrence displayed)
        action.interested_volunteers.add(self.volunteer1)
        occurrence.interested_volunteers.add(self.volunteer1)

        # 3) coordinator sees list of action.interested_volunteers, and assigns ONE volunteer
        assignment = ActionOccurrenceVolunteerAssignment.objects.create(
            action_occurrence=occurrence, volunteer=self.volunteer1,
            status='assigned'
        )
        action.interested_volunteers.remove(self.volunteer1)
        action.assigned_volunteers.add(self.volunteer1)
        occurrence.assigned_volunteers.add(self.volunteer1)

        # 4) optional: volunteer makes contact
        occurrence.volunteer_made_contact_on = now
        occurrence.save()

        # 5) volunteer finishes action, adds feedback
        assignment.status = 'feedback_given'
        assignment.completed_datetime = datetime.datetime.now()
        assignment.time_taken = datetime.timedelta(hours=1)
        assignment.repetition_requested = True  # "I'm able to help again: [Y]"
        assignment.save()

        ActionOccurrenceVolunteerAssignmentFeedback.objects.create(
            assignment=assignment, notes='lovely dog!'
        )
        action.scheduling_type = 'ongoing'  # or action.status?
        action.save()

        '''
        UI questions:
        - "this person said they would like help with this again" [Y/N]
                - "I'm able to help again" [Y/N]
                - "Do you know when this help is needed next?" [Y/N]
                    - "Choose date/time" [date/time]
        
        difficult:
            can't help
            help is needed 
                but don't know when
        
        
        '''

        wants_help_again = False
        able_to_help_again = True
        next_date = None

        if wants_help_again:
            if able_to_help_again:
                if next_date:
                    pass  # create occurrence to current volunteer
                else:
                    pass  # Action changes to 'ongoing' with no future occurrences
            else:
                if next_date:
                    pass  # create occurrence, with no-one assigned, remove volunteer from action
                else:
                    pass  # remove volunteer from action, flag to coordinator to find/assign new volunteer
        else:
            pass
            # 'close' action




        if date_next_date_specified:
            new_occurrence = ActionOccurrence.objects.create(
                action=action, due_datetime=now
            )
            if able_to_help_again:
                new_occurrence.assigned_volunteers.add(self.volunteer1)

        # 6) volunteer repeats action, retroactively adds feedback (and implicitly, an occurrence)
        if date_next_date_specified is False:
            new_occurrence = ActionOccurrence.objects.create(
                action=action, due_datetime=now
            )
            new_occurrence.assigned_volunteers.add(self.volunteer1)

        assignment.status = 'feedback_given'
        assignment.completed_datetime = datetime.datetime.now()
        assignment.time_taken = datetime.timedelta(hours=1)
        assignment.repetition_requested = True  # "I'm able to help again: [Y]"
        assignment.save()
        ActionOccurrenceVolunteerAssignmentFeedback.objects.create(
            assignment=assignment, notes='lovely dog!'
        )

    def group_leafleting__once_off_with_due_date(self):

        volunteer1 = create_volunteer(
            1, self.help_types.values(), []
        )
        volunteer2 = create_volunteer(
            2, self.help_types.values(), []
        )
        volunteer3 = create_volunteer(
            3, self.help_types.values(), []
        )
        volunteers = [volunteer1, volunteer2, volunteer3]


        weeks_time = datetime.datetime.now() + datetime.timedelta(days=7)
        now = datetime.datetime.now()

        # 1) coordinator creates leafleting Action for Organisation
        action = ActionV2.objects.create(
            action_priority='medium', organisation=self.organisation1,  # todo: orgs?
            help_type=self.help_types['leafleting']
        )
        action.requirements.add([])  # nothing

        # 2) coordinator is forced to create an occurrence
        occurrence = ActionOccurrence.objects.create(
            action=action, status='pending', due_datetime=weeks_time,
            min_volunteers=3, max_volunteers=10
        )

        # 2) volunteers express their interest in action (with occurrence displayed)
        for v in volunteers:
            action.interested_volunteers.add(v)
            occurrence.interested_volunteers.add(v)

        # 3) coordinator sees list of action.interested_volunteers, and assigns 3-10 volunteers
        assignments = []
        for v in volunteers:
            a = ActionOccurrenceVolunteerAssignment.objects.create(
                action_occurrence=occurrence, volunteer=v,
                status='assigned'
            )
            assignments.append(a)
            action.interested_volunteers.remove(v)
            action.assigned_volunteers.add(v)
            occurrence.assigned_volunteers.add(v)

        # 4) optional: volunteer makes contact
        for v in volunteers:
            occurrence.volunteer_made_contact_on = now
            occurrence.save()

        # 5) volunteers does action, adds feedback (1st time)
        for assignment in assignments:

            assignment.status = 'feedback_given'
            assignment.completed_datetime = datetime.datetime.now()
            assignment.time_taken = datetime.timedelta(hours=1)
            assignment.repetition_requested = True  # "I'm able to help again: [Y]"
            assignment.save()

            ActionOccurrenceVolunteerAssignmentFeedback.objects.create(
                assignment=assignment, notes='lovely dog!'
            )
            action.scheduling_type = 'ongoing'  # or action.status?
            action.save()

            wants_help_again = False
            able_to_help_again = True
            next_date = None

            if wants_help_again:
                if able_to_help_again:
                    if next_date:
                        pass  # create occurrence to current volunteer
                    else:
                        pass  # Action changes to 'ongoing' with no future occurrences
                else:
                    if next_date:
                        pass  # create occurrence, with no-one assigned, remove volunteer from action
                    else:
                        pass  # remove volunteer from action, flag to coordinator to find/assign new volunteer
            else:
                pass
                # 'close' action




    def _dog_walking_setup(self, recurring):

        curr_date = datetime.datetime.now() + datetime.timedelta(days=7)
        dates = [curr_date]

        if recurring:
            for i in range(3):
                dates.append(
                    dates[-1] + datetime.timedelta(days=7)
                )

        # 1) coordinator creates dog-walking Action for Resident
        action = ActionV2.objects.create(
            resident=self.resident1, action_priority='medium',
            help_type=self.help_types['dog_walking']
        )
        action.requirements.add(self.reqs['experience_with_dogs'])
        # side-effect of new action-occureence
        occurrences = []
        for date in dates:
            occ = ActionOccurrence.objects.create(
                action=action, status='pending', due_datetime=date
            )
            occurrences.append(occ)

        # 2) volunteer expresses interest in action (how to assign occurrence?)
        occurrences[0].interested_volunteers.add(self.volunteer1)

        # 3) coordinator sees pending volunteer approval, and assigns them
        assignment = ActionOccurrenceVolunteerAssignment.objects.create(
            action_occurrence=occurrences[0], volunteer=self.volunteer1,
            status='assigned'
        )

        # 4) volunteer informs us they have made contact
        assignment.volunteer_made_contact_on = datetime.datetime.now()
        assignment.save()
        return assignment, occurrences

    def test_dog_walking__no_repetition(self):
        assignment, _ = self._dog_walking_setup(False)

        # 5) volunteer finishes action, adds feedback
        assignment.feedback_notes = 'lovely dog!'
        assignment.status = 'feedback_given'
        assignment.completed_datetime = datetime.datetime.now()
        assignment.time_taken = datetime.timedelta(hours=1)
        assignment.repetition_requested = False
        assignment.save()

    def test_dog_walking__with_repetition(self):
        assignment, occurrences = self._dog_walking_setup(True)

        # 5) volunteer finishes action, adds feedback, assigns themselves to next occurrence
        assignment.feedback_notes = 'lovely dog!'
        assignment.status = 'feedback_given'
        assignment.completed_datetime = datetime.datetime.now()
        assignment.time_taken = datetime.timedelta(hours=1)
        assignment.repetition_requested = True
        assignment.save()

        if assignment.action.allow_auto_assign_on_repetition:
            next_occurrence = assignment.action_occurrence.get_next()
            ActionOccurrenceVolunteerAssignment.objects.create(
                action_occurrence=next_occurrence, volunteer=self.volunteer1,
                status='pending'
            )



'''
class ActionOccurrenceVolunteerAssignment(models.Model):

    action_occurrence = models.ForeignKey('ActionOccurrence', on_delete=models.PROTECT)
    volunteer = models.ForeignKey(user_models.Volunteer, on_delete=models.PROTECT)

    status = models.CharField(
        max_length=30, default='assigned',
        choices=ACTION_ASSIGNMENT_STATUS_CHOICES
    )
    created_datetime = models.DateTimeField(auto_now_add=True)

    # feedback fields
    volunteer_made_contact_on = models.DateTimeField(null=True, blank=True)
    feedback_notes = models.TextField(max_length=999, blank=True, null=True)
    repetition_requested = models.BooleanField(default=False)

    completed_datetime = models.DateTimeField(null=True, blank=True)
    time_taken = models.DurationField(blank=True, null=True)


class ActionOccurrence(models.Model):

    action = models.ForeignKey('ActionV2', on_delete=models.PROTECT)
    status = models.CharField(
        max_length=30, choices=ActionOccurrenceStatus.STATUSES,
        default=ActionOccurrenceStatus.PENDING,
        help_text="What's the status of this action-occurrence?"
    )
    due_datetime = models.DateTimeField(
        verbose_name="Due", help_text="When should the action-occurrence be completed by?"
    )

    min_volunteers = models.IntegerField(default=1)
    max_volunteers = models.IntegerField(default=1)

    interested_volunteers = models.ManyToManyField(
        user_models.Volunteer, blank=True, related_name="actions_interested_in2",
        help_text="Volunteers who have expressed interest in completing the action.."
    )
    assigned_volunteers = models.ManyToManyField(
        user_models.Volunteer, blank=True,
        through=ActionOccurrenceVolunteerAssignment,
        related_name="actions_assigned2",
        help_text="Volunteers who have expressed interest in completing the action.."
    )



class ActionV2(models.Model):

    external_action_id = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="The ID of the action in an external system"
    )
    resident = models.ForeignKey(
        user_models.Resident, on_delete=models.PROTECT,
        null=True, help_text="Who made the request?"
    )

    min_volunteers = models.IntegerField(default=1)
    max_volunteers = models.IntegerField(default=1)

    action_priority = models.CharField(
        max_length=30, choices=ActionPriorityV2.PRIORITIES,
        default=ActionPriorityV2.MEDIUM,
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
    allow_auto_assign = models.BooleanField(default=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)



    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')


class Volunteer(UserProfileMixin, Person):
    """Concrete class for those who can offer help."""
    profile_related_name = 'volunteer'
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.SET_NULL, related_name=profile_related_name)
    external_volunteer_id = models.CharField(
        max_length=50, null=True, blank=True, help_text="The ID of the volunteer in an external system")
    dbs_number = models.CharField(max_length=12, null=True, blank=True,
                                  help_text="The user's DBS certificate number, if they have one.")

'''