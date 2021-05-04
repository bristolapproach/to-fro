from rest_framework import mixins, viewsets

class BaseToFroViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   #mixins.UpdateModelMixin,
                   #mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    pass