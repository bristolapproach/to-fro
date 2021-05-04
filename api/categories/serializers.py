from rest_framework import serializers
from .models import HelpType, Requirement


class HelpTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpType
        fields = '__all__'


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'
