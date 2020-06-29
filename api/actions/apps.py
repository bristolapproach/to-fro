from django.apps import AppConfig


class ActionsConfig(AppConfig):
    name = 'actions'
    verbose_name = "Actions"

    # Import the signals when Django is ready.
    def ready(self):
        import actions.signals
