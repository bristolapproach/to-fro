from rest_framework import serializers
from .models import Volunteer, Coordinator, Resident

class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = ['pk', 'first_name', 'last_name', 'phone', 'phone_secondary', 'email', 'notes',
                  'person_ptr_id', 'user_without_account', 'user_id', 'external_volunteer_id',
                  'time_given', 'daily_digest_optin', 'weekly_digest_optin', 'requirements',
                  'help_types']


class CoordinatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coordinator
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resident
        fields = '__all__'


