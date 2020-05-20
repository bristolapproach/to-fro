from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "People"

    # Import the signals when Django is ready.
    def ready(self):
        import users.signals
