from rest_framework import serializers
from .models import Volunteer, Coordinator, Resident

class VolunteerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volunteer
        fields = '__all__'


class CoordinatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coordinator
        fields = '__all__'


class ResidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Resident
        fields = '__all__'


