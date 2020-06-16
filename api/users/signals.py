from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from categories.models import HelpType, Ward
from users.models import Volunteer, Coordinator

import logging
logger = logging.getLogger(__name__)


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


User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="UserSaved")
def post_save_user(sender, instance, created, **kwargs):
    if not created:
        # Need to check before accessing relations
        # as it would throw a NotFoundException
        if (instance.is_volunteer):
            update_profile_info(instance.volunteer, instance)
        if (instance.is_coordinator):
            update_profile_info(instance.coordinator, instance)


def update_profile_info(profile, user):
    # Little security to not wipe things
    # When the admin user is created
    if user.first_name:
        profile.first_name = user.first_name
    if user.last_name:
        profile.last_name = user.last_name
    if user.email:
        profile.email = user.email
    profile.save()


@receiver(post_delete, sender=Coordinator, dispatch_uid="CoordinatorDeleted")
def post_delete_coordinator(sender, instance, **kwargs):
    """
    Automatically delete users if there's no profile attached to them
    or adjust privileges
    """
    if not instance.user.is_volunteer:
        instance.user.delete()
    else:
        # Remove superuser and staff privileges
        # for non-coordinator users
        user = instance.user
        user.is_staff = False
        user.is_superuser = False
        user.coordinator = None
        user.save()


@receiver(post_delete, sender=Volunteer, dispatch_uid="VolunteerDeleted")
def post_delete_user_profile(sender, instance, **kwargs):
    """
    Automatically delete users if there's no profile attached to them
    """
    if not instance.user.is_coordinator:
        instance.user.delete()
