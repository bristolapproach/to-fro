from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    # Import the signals when Django is ready.
    def ready(self):
        import core.signals
