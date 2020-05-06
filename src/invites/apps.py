from django.apps import AppConfig


class InvitesConfig(AppConfig):
    name = 'invites'

    # Import the signals when Django is ready.
    def ready(self):
        import invites.signals
