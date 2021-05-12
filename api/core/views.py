from rest_framework import mixins, viewsets
from rest_framework.decorators import action

class BaseToFroViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   #mixins.UpdateModelMixin,
                   #mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `retrieve()` and `list()` actions.
    """
    pass

class IsInMixin():
    @action(methods=['get'], detail=False, url_path='isin/(?P<pks>[0-9,]+)')
    def isin(self, request, pks=None):
        pks = pks.split(',')
        pks = [int(pk) for pk in pks]
        self.queryset = self.queryset.filter(pk__in=pks)
        print(self.queryset.count())
        return self.list(request)
