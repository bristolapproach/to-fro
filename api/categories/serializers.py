from rest_framework import serializers
from .models import HelpType, Requirement, Ward, ReferralType


class HelpTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpType
        fields = '__all__'


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = '__all__'


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'


class ReferralTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralType
        fields = '__all__'
