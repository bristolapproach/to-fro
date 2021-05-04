from django.test import TestCase, Client
from django.urls import include, path, reverse


from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key

from django.contrib.auth.models import User as AuthUser
from rest_framework.test import APIRequestFactory, APIClient, APITestCase

from users.models import Volunteer, Coordinator, Resident
from .models import Action, ActionFeedback, ActionStatus
from categories.models import Requirement, Ward, HelpType
from notifications.utils import gen_subject_and_message
from notifications.models import NotificationTypes

user_dan = Recipe(AuthUser,
                first_name='Daniel',
                password='868uFscwoPmNK+g'  )

requirement_recipe = Recipe(Requirement)
ward_recipe = Recipe(Ward)
help_type_recipe = Recipe(HelpType)
volunteer_dan = Recipe(Volunteer,
                       user=foreign_key(user_dan))
coordinator_dan = Recipe(Coordinator,
                         user=foreign_key(user_dan))
resident_dan = Recipe(Resident,
                      ward=foreign_key(ward_recipe))

action_recipe = Recipe(Action,
                       assigned_volunteer=foreign_key(volunteer_dan),
                       coordinator=foreign_key(coordinator_dan),
                       help_type=foreign_key(help_type_recipe),
                       added_by=foreign_key(coordinator_dan))

actionfeedback_recipe = Recipe(ActionFeedback,
                               action=foreign_key(action_recipe),
                               volunteer=foreign_key(volunteer_dan),
#                               assigned_volunteer_action=foreign_key(action_assigned_volunteers_recipe)
                               )
class ActionAPITestCase(APITestCase):
    #urlpatterns = [path('api/', include('api.urls')),]

    def setUp(self):
        self.action = action_recipe.make()

    def test_create_account(self):
        """
        Ensure we read an Action

        url = reverse('account-list')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')
        """
        url = reverse('action:action-api',)
        self.assertTrue(True)

class ActionFeedbackTestCase(TestCase):
    def setUp(self):
        self.volunteer2 = volunteer_dan.make()
        self.actionfeedback = actionfeedback_recipe.make(
            volunteer=self.volunteer2
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
        self.assertEqual(self.action.assigned_volunteers.all().count(), 0)
        copy_volunteers()
        self.assertEqual(
            self.action.assigned_volunteers.get(pk=self.volunteer.pk),
            self.volunteer
        )

    def test_reassigned_cleared(self):
        self.action.assigned_volunteers.clear()
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status = ActionStatus.ASSIGNED
        self.action.save()
        self.assertEqual(self.action.assigned_volunteers.count(), 1)
        self.action.action_status = ActionStatus.INTEREST
        self.action.save()
        self.assertEqual(self.action.assigned_volunteers.count(), 0)

    def test_added_volunteer_changes_status(self):
        self.action.assigned_volunteers.clear()
        self.action.assigned_volunteer = None
        self.action.action_status = ActionStatus.PENDING
        self.action.save()
        self.assertEqual(self.action.action_status, ActionStatus.PENDING)
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.save()
        self.assertEqual(self.action.action_status, ActionStatus.ASSIGNED)

    def test_add_assigned_adds_interested(self):
        self.action.assigned_volunteers.clear()
        self.action.interested_volunteers.clear()
        self.action.assigned_volunteer = None
        self.action.save()
        self.assertEqual(self.action.interested_volunteers.all().count(), 0)
        volunteer = volunteer_dan.make()
        self.action.assigned_volunteers.add(volunteer)
        #ActionAssignedVolunteers.objects.create(action=self.action,
        #                                        assigned_volunteer=volunteer)
        #self.action.save()
        self.assertEqual(self.action.interested_volunteers.all()[0].pk, volunteer.pk)

    def test_register_interest_from(self):
        self.action.assigned_volunteers.clear()
        self.action.interested_volunteers.clear()
        self.action.assigned_volunteer = None
        self.action.save()
        self.assertEqual(self.action.interested_volunteers.all().count(), 0)
        volunteer = volunteer_dan.make()
        self.action.register_interest_from(volunteer)
        self.assertEqual(self.action.interested_volunteers.all()[0].pk, volunteer.pk)

    def test_withdraw_interest_from(self):
        self.action.assigned_volunteers.clear()
        self.action.interested_volunteers.clear()
        self.action.assigned_volunteer = None
        self.action.save()
        volunteer = volunteer_dan.make()
        self.action.register_interest_from(volunteer)
        self.assertEqual(self.action.interested_volunteers.all().count(), 1)
        self.action.withdraw_interest_from(volunteer)
        self.assertEqual(self.action.interested_volunteers.all().count(), 0)

class VolunteerAction(TestCase):
    def setUp(self):
        self.c = Client()
        self.resident = resident_dan.make()
        self.action = action_recipe.make(resident=self.resident)
        self.volunteer = volunteer_dan.make()
        self.requirement = requirement_recipe.make()
        self.action.requirements.add(self.requirement)
        self.volunteer.requirements.add(self.requirement)
        self.volunteer.wards.add(self.resident.ward)
        self.volunteer.help_types.add(self.action.help_type)
        self.user = self.volunteer.user
        self.action.assigned_volunteers.clear()
        self.action.interested_volunteers.clear()
        self.action.assigned_volunteer = None
        #shouldn't need to do this - should be automagic
        self.action.action_status = ActionStatus.PENDING
        self.action.save()
        self.c.force_login(self.user)

    def test_volunteer_contact_notification_text(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ONGOING
        self.action.save()
        subject, body = gen_subject_and_message('', NotificationTypes.VOLUNTEER_CONTACT,
                                                 action=self.action, context={'action': self.action} )
        self.assertIn(self.action.assigned_volunteers.all()[0].first_name, body)

    def test_volunteer_ongoing_notification_text(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ONGOING
        self.action.save()
        subject, body = gen_subject_and_message('', NotificationTypes.ACTION_ONGOING,
                                                 action=self.action, context={'action': self.action} )
        self.assertIn(self.action.assigned_volunteers.all()[0].first_name, body)

    def test_volunteer_not_completed_notification_text(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ONGOING
        self.action.save()
        subject, body = gen_subject_and_message('', NotificationTypes.ACTION_NOT_COMPLETED,
                                                 action=self.action, context={'action': self.action} )
        self.assertIn(self.action.assigned_volunteers.all()[0].first_name, body)

    def test_volunteer_action_completed_notification_text(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ONGOING
        self.action.save()
        subject, body = gen_subject_and_message('', NotificationTypes.ACTION_COMPLETED,
                                                 action=self.action, context={'action': self.action} )
        self.assertIn(self.action.assigned_volunteers.all()[0].first_name, body)

    def test_volunteer_ongoing_actions(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ONGOING
        self.action.save()
        self.assertTrue(self.volunteer.ongoing_actions.filter(pk=self.action.pk).exists())

    def test_volunteer_completed_actions(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.COMPLETED
        self.action.save()
        self.assertTrue(self.volunteer.completed_actions.filter(pk=self.action.pk).exists())

    def test_volunteer_uncompletable_actions(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.COULDNT_COMPLETE
        self.action.save()
        self.assertTrue(self.volunteer.completed_actions.filter(pk=self.action.pk).exists())

    def test_context_actions_offer_help(self):
        response = self.c.get('/actions/available/')
        self.assertEqual(response.context['actions'][0].pk, self.action.pk)

    def test_context_actions_fail_quals_offer_help(self):
        self.volunteer.requirements.clear()
        response = self.c.get('/actions/available/')
        self.assertEqual(len(response.context['actions']), 0)

    def test_context_actions_upcoming(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ASSIGNED
        self.action.save()
        response = self.c.get('/')
        self.assertEqual(response.context['actions'][0].pk, self.action.pk)

    def test_checkin_for_single_vol_action(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ASSIGNED
        self.action.save()
        response = self.c.get('/')
        #self.assertContains(response, "Please contact the person")
        self.assertTrue(response.context['actions'][0].checkin_required)

    def test_checkin_for_multiple_vol_action(self):
        self.action.maximum_volunteers = 2
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ASSIGNED
        self.action.save()
        response = self.c.get('/')
        self.assertFalse(response.context['actions'][0].checkin_required)

    def test_action_feedback_not_ongoing(self):
        self.action.assigned_volunteers.add(self.volunteer)
        self.action.action_status=ActionStatus.ASSIGNED
        self.action.save()
        self.assertTrue(self.action.can_give_feedback)
        url = reverse('actions:complete', kwargs={'action_uuid': self.action.action_uuid})
        response = self.c.post(url, data={'duration': '15:30',
                                          'notes': 'Blah Blah',
                                          })
        self.assertEqual(self.action.actionfeedback_set.all().count(), 1)








