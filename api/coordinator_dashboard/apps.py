from django.apps import AppConfig


class CoordinatorDashboardConfig(AppConfig):
    name = 'coordinator_dashboard'

    # Import the signals when Django is ready.
    def ready(self):
        import notifications.signals
