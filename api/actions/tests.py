import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from actions.models import (
    ActionV2, ActionOccurrence, ActionOccurrenceFeedback, ActionPeriod
)
from categories.models import HelpType, Requirement
from users.models import Volunteer, Resident, Coordinator, ResidentVolunteerRelationship


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

    def dog_walking_unscheduled(self):

        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(days=7)

        # 1) coordinator creates dog-walking Action for Resident
        action = ActionV2.objects.create(
            resident=self.resident1, action_priority='medium',
            help_type=self.help_types['dog_walking']
        )
        action.requirements.add(self.reqs['experience_with_dogs'])

        # 2) volunteer expresses interest in action
        action.interested_volunteers.add(self.volunteer1)

        # 3) coordinator sees list of action.interested_volunteers, and assigns ONE volunteer
        action.assigned_volunteers.add(self.volunteer1)

        # 4) optional: volunteer notifies us they have made contact
        ResidentVolunteerRelationship.objects.create(
            volunteer=self.volunteer1, resident=self.resident1,
            first_contact_datetime=now
        )

        # 5) volunteer finishes, creating a retrospective ActionOccurrence with feedback
        # (if not ActionOccurrence.objects.filter(action=action, volunteer=self.volunteer1).exists())
        occurrence = ActionOccurrence.object.create(
            action=action, volunteer=self.volunteer1,
            occurrence_type='retrospectively_logged'
        )
        resident_wants_help_again = True
        volunteer_able_to_help_again = True
        expected_next_date = next_week
        feedback = ActionOccurrenceFeedback.objects.create(
            occurrence=occurrence,
            time_taken=datetime.timedelta(hours=2), completed_datetime=now,
            resident_wants_help_again=resident_wants_help_again,
            volunteer_able_to_help_again=volunteer_able_to_help_again,
            expected_next_date=expected_next_date
        )
        occurrence.status = 'complete'
        self.handle_feedback(action)

    def dog_walking_scheduled(self):

        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(days=7)

        # 1) coordinator creates dog-walking Action for Resident
        action = ActionV2.objects.create(
            resident=self.resident1, action_priority='medium',
            help_type=self.help_types['dog_walking']
        )
        action.requirements.add(self.reqs['experience_with_dogs'])

        # 2) coordinator schedules date for Action to occur (or be due by)
        occurrence = ActionOccurrence.object.create(
            action=action, volunteer=self.volunteer1,
            occurrence_type='scheduled_in_advance',
            due_datetime=next_week
        )

        # 2) volunteer expresses interest in action
        action.interested_volunteers.add(self.volunteer1)

        # 3) coordinator sees list of action.interested_volunteers, and assigns ONE volunteer
        action.assigned_volunteers.add(self.volunteer1)

        # 4) optional: volunteer notifies us they have made contact
        ResidentVolunteerRelationship.objects.create(
            volunteer=self.volunteer1, resident=self.resident1,
            first_contact_datetime=now
        )

        # 5) volunteer finishes, adds feedback to the existing ActionOccurrence
        occurrence = ActionOccurrence.objects.filter(
            action=action, volunteer=self.volunteer1
        ).first()

        resident_wants_help_again = True
        volunteer_able_to_help_again = True
        expected_next_date = next_week
        feedback = ActionOccurrenceFeedback.objects.create(
            occurrence=occurrence,
            time_taken=datetime.timedelta(hours=2), completed_datetime=now,
            resident_wants_help_again=resident_wants_help_again,
            volunteer_able_to_help_again=volunteer_able_to_help_again,
            expected_next_date=expected_next_date
        )
        occurrence.status = 'complete'
        self.handle_feedback(action)

    def handle_feedback(self, action):
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
        resident_wants_help_again = False
        volunteer_able_to_help_again = True
        next_date = None

        if not resident_wants_help_again:
            action.status = 'closed'
            return

        due_datetime = None
        if next_date:
            due_datetime = due_datetime

        if volunteer_able_to_help_again:
            status = 'assigned_pending'
            volunteer = self.volunteer1
        else:
            status = 'unassigned'  # this should be flagged to coordinator
            volunteer = None

        ActionOccurrence.objects.create(
            action=action, status=status, volunteer=volunteer,
            due_datetime=due_datetime
        )

        '''
                                     ---- the above is equivalent to: ------- 
        if resident_wants_help_again:
            if volunteer_able_to_help_again:
                # create new ActionOccurrence (with volunteer assigned: 'assigned_pending')
                if next_date:
                    pass  # set occurrence.due_datetime
                else:
                    pass  # leave occurrence.due_datetime = None
            else:
                if next_date:
                    pass  # create ActionOccurrence (unassigned), set volunteer = None, set due_datetime = next_date
                else:
                    pass  # create ActionOccurrence (unassigned), set volunteer = None, set due_datetime = None
        else:
            pass
            # 'close' action
        '''

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

        now = datetime.datetime.now()
        next_week = now + datetime.timedelta(days=7)

        # 1) coordinator creates leafleting Action for Organisation
        action = ActionV2.objects.create(
            action_priority='medium', organisation=self.organisation1,
            help_type=self.help_types['leafleting']
        )
        action.requirements.add([])  # nothing

        # 2) coordinator is forced to create an ActionPeriod
        period = ActionPeriod.objects.create(
            action=action, start_datetime=now, end_datetime=next_week,
            min_volunteers=3, max_volunteers=10
        )

        # 2) volunteers express their interest in action/period (with date(s) displayed)
        for v in volunteers:
            period.interested_volunteers.add(v)

        # 3) coordinator sees list of period.interested_volunteers, and assigns 3-10 volunteers
        # this creates an ActionOccurrence for each volunteer
        period.assigned_volunteers.add(*volunteers)
        period.interested_volunteers.remove(*volunteers)
        for v in volunteers:
            ActionOccurrence.objects.create(
                action=action, action_period=period, volunteer=v,
                occurrence_type='scheduled_in_advance',
                due_datetime=period.end_datetime  # set due date to end of period?
                # no start date?
            )
            ResidentVolunteerRelationship.objects.get_or_create(
                resident=self.resident1, volunteer=v
            )

        # 4) optional: volunteer makes contact
        for v in volunteers:
            rel = ResidentVolunteerRelationship.objets.get(
                resident=self.resident1, volunteer=v
            )
            rel.volunteer_made_contact_on = now
            rel.save()

        # 5) volunteers performs action, adds feedback
        for v in volunteers:
            occurrence = ActionOccurrence.objects.filter(
                action=action, volunteer=v
            ).last()
            ActionOccurrenceFeedback.objects.create(
                occurrence=occurrence, time_taken=datetime.timedelta(hours=2),
                completed_datetime=next_week
            )

        # do we ask any questions? where do we configure these?
