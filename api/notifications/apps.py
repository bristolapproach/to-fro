from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    # Import the signals when Django is ready.
    def ready(self):
        import notifications.signals
