from rest_framework import viewsets
from .serializers import HelpTypeSerializer, RequirementSerializer
from .models import HelpType, Requirement
from core.views import BaseToFroViewSet


class HelpTypeViewSet(BaseToFroViewSet):
    queryset = HelpType.objects.all()
    serializer_class = HelpTypeSerializer


class RequirementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
