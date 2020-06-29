from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from categories.models import HelpType, Ward
from users.models import Volunteer, Settings

User = get_user_model()


@receiver(post_save, sender=HelpType, dispatch_uid="HelpTypeOptIn")
@receiver(post_save, sender=Ward, dispatch_uid="WardOptIn")
def post_save_category(sender, instance, created, **kwargs):
    """
    Automatically opt-in all volunteers to new Wards and HelpTypes
    so they see the new actions in their listing.
    """
    if created:
        instance.volunteers.set(Volunteer.objects.all())
        instance.save()


@receiver(post_save, sender=User, dispatch_uid="CreateUserSettings")
def create_user_settings(sender, instance, created, **kwargs):
    """
    Ensures all users have a Settings object when created
    """
    if created:
        Settings(user=instance).save()
