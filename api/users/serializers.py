from rest_framework import serializers
from .models import Volunteer, Coordinator, Resident

class VolunteerSerializer(serializers.ModelSerializer):

    def __init__( self, *args, **kwargs ):
        #raise Exception
        super(VolunteerSerializer, self).__init__(*args, **kwargs)
        if not kwargs['context']['view'].detail:
            self.fields.pop('actions_assigned_to')


    class Meta:
        model = Volunteer
        fields = ['pk', 'first_name', 'last_name', 'phone', 'phone_secondary', 'email', 'notes',
                  'person_ptr_id', 'user_without_account', 'user_id', 'external_volunteer_id',
                  'time_given', 'daily_digest_optin', 'weekly_digest_optin', 'requirements',
                  'help_types', 'actions_assigned_to', 'wards']


class CoordinatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coordinator
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):

    def __init__( self, *args, **kwargs ):
        super(ResidentSerializer, self).__init__(*args, **kwargs)
        if not kwargs['context']['view'].detail:
            self.fields.pop('requested_actions')


    class Meta:
        model = Resident
        fields = ['id', 'first_name', 'last_name', 'phone', 'phone_secondary', 'email',
        'notes', 'address_line_1', 'address_line_2', 'address_line_3', 'postcode',
        'internet_access', 'smart_device', 'confident_online_shopping', 'requested_actions',
        'confident_online_comms', 'shielded', 'time_received', 'data_consent_date', 'ward']


