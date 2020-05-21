from django.contrib import admin


class ModelAdminWithExtraContext(admin.ModelAdmin):
    """
    Base class for creating an admin that automatically adds some
    extra context to the add and change views
    """

    def extra_context(self, object_id=None):
        """
        To be overriden by the extending classes
        """
        return {}

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context())
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update(self.extra_context(object_id=object_id))
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
