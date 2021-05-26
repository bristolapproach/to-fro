from django.urls import path, include
from .models import Action, Referral, Organisation
#from users.serializers import VolunteerSerializer
from rest_framework import serializers

# Serializers define the API representation.


class ActionSerializer(serializers.ModelSerializer):

    def __init__( self, *args, **kwargs ):
        #raise Exception
        super(ActionSerializer, self).__init__(*args, **kwargs)
        if not kwargs['context']['view'].detail:
            self.fields.pop('potential_volunteer_ids')
            self.fields.pop('actionfeedback_set')

    class Meta:
        model = Action
        fields = ['id', 'external_action_id', 'added_by', 'coordinator', 'call_datetime',
                  'call_duration', 'resident_id', 'requested_datetime', 'assigned_volunteers',
                  'action_status', 'action_priority', 'public_description', 'private_description',
                  'help_type_id', 'volunteer_made_contact_on', 'assigned_date', 'completed_date',
                  'action_uuid', 'time_taken', 'minimum_volunteers', 'maximum_volunteers',
                  'potential_volunteer_ids', 'actionfeedback_set']


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'




'''
class OldActionListSerializer(serializers.ModelSerializer):
    resident = serializers.StringRelatedField(many=False)
    help_type = serializers.StringRelatedField(many=False)
    action_status = serializers.CharField(source='get_action_status_display')

    class Meta:
        model = Action
        fields = [
            'pk', 'resident', 'help_type', 'requested_datetime', 'volunteer_made_contact_on',
            'action_status', 'time_taken'
        ]
        #depth = 1


class OldActionSerializer(serializers.ModelSerializer):
    interested_volunteers = serializers.StringRelatedField(many=True)
    assigned_volunteers = VolunteerSerializer(many=True, read_only=True)

    class Meta:
        model = Action
        fields = [
            'id', 'resident', 'help_type', 'action_priority', 'requested_datetime',
            'volunteer_made_contact_on', 'coordinator', 'minimum_volunteers', 'maximum_volunteers',
            'requirements', 'external_action_id', 'public_description', 'private_description',
            'action_status', 'time_taken', 'added_by', 'call_datetime', 'call_duration',
            'assigned_volunteers', 'interested_volunteers', 'assigned_date', 'completed_date',
        ]
        depth = 1
'''

