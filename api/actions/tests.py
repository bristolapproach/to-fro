from django.test import TestCase


from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key

from django.contrib.auth.models import User as AuthUser
from users.models import Volunteer, Coordinator
from .models import Action, ActionVolunteers, ActionFeedback

user_dan = Recipe(AuthUser,
                first_name='Daniel')

volunteer_dan = Recipe(Volunteer,
                       user=foreign_key(user_dan))
coordinator_dan = Recipe(Coordinator,
                         user=foreign_key(user_dan))

action_recipe = Recipe(Action,
                       assigned_volunteer=foreign_key(volunteer_dan),
                       coordinator=foreign_key(coordinator_dan),
                       added_by=foreign_key(coordinator_dan))

actionfeedback_recipe = Recipe(ActionFeedback,
                               action=foreign_key(action_recipe),
                               volunteer=foreign_key(volunteer_dan))

class ActionFeedbackTestCase(TestCase):
    def setUp(self):
        self.volunteer2 = volunteer_dan.make()
        self.actionfeedback = actionfeedback_recipe.make(
            volunteer=self.volunteer2
        )

    def test_migrate(self):
        from .utils import copy_feedback
        copy_feedback()
        #import pdb; pdb.set_trace()
        self.assertEqual(
            ActionFeedback.objects.get(pk=self.actionfeedback.pk).action_volunteer.volunteer.pk,
            self.volunteer2.pk
        )


class ActionTestCase(TestCase):

    def setUp( self ):
        #auth_user = baker.make(AuthUser, first_name='Daniel')
        #user = baker.make('users.Volunteer',
        #                  user=auth_user)
        #self.volunteer = volunteer_dan.make()
        self.action = action_recipe.make()
        self.volunteer = self.action.assigned_volunteer

    def test_assigned_migration(self):
        from .utils import copy_volunteers
        self.assertEqual(self.action.volunteers.all().count(), 0)
        copy_volunteers()
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).assigned, True)
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).interested, False)

    def test_interested_migration(self):
        from .utils import copy_volunteers
        self.assertEqual(self.action.volunteers.all().count(), 0)
        self.action.assigned_volunteer = None
        self.action.save()
        self.action.interested_volunteers.add(self.volunteer)
        copy_volunteers()
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).assigned, False)
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).interested, True)

    def test_both_migration(self):
        from .utils import copy_volunteers
        self.assertEqual(self.action.volunteers.all().count(), 0)
        self.action.interested_volunteers.add(self.volunteer)
        copy_volunteers()
        #import pdb; pdb.set_trace()
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).assigned, True)
        self.assertEqual(ActionVolunteers.objects.get(
            action=self.action,volunteer=self.volunteer).interested, True)

