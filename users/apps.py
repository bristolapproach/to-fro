from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # Import the signals when Django is ready.
    def ready(self):
        import users.signals
