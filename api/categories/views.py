from rest_framework import viewsets
from .serializers import HelpTypeSerializer, RequirementSerializer, WardSerializer, ReferralTypeSerializer
from .models import HelpType, Requirement, Ward, ReferralType
from core.views import BaseToFroViewSet


class HelpTypeViewSet(BaseToFroViewSet):
    queryset = HelpType.objects.all()
    serializer_class = HelpTypeSerializer


class ReferralTypeViewSet(BaseToFroViewSet):
    queryset = ReferralType.objects.all()
    serializer_class = ReferralTypeSerializer


class RequirementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


