import logging
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from categories.models import HelpType, Ward
from users.models import Volunteer, Coordinator,  Settings
import os

User = get_user_model()

logger = logging.getLogger(__name__)

###
# Wards and help types
###


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

###
# Settings profile
###


@receiver(post_save, sender=User, dispatch_uid="CreateUserSettings")
def create_user_settings(sender, instance, created, **kwargs):
    """
    Ensures all users have a Settings object when created
    """
    if created:
        Settings(user=instance).save()

###
# Personal information synchronisation
###


USER_FIELDS_TO_SYNC = (
    'first_name',
    'last_name',
    'email'
)

PROFILES_FIELDS_TO_SYNC = USER_FIELDS_TO_SYNC + (
    'phone',
    'phone_secondary'
)


def some(iterable, function):
    """
    Alternative to the native `any()` which
    accepts a lambda for computing whether to return True
    """
    for value in iterable:
        if function(value):
            return True
    return False


@receiver(post_save, sender=Volunteer, dispatch_uid="VolunteerSaved")
@receiver(post_save, sender=Coordinator, dispatch_uid="CoordinatorSaved")
def post_save_volunteer(sender, instance, created, **kwargs):
    if not created:
        changed_fields = instance.tracker.changed().keys()
        # Sync can only happen for users that have an account
        if not instance.user_without_account:
            # Sync with the user info
            if some(USER_FIELDS_TO_SYNC, lambda field_name: field_name in changed_fields) and sync_user(instance, instance.user):
                instance.user.save()

            # Sync with a potential other profile
            if some(PROFILES_FIELDS_TO_SYNC, lambda field_name: field_name in changed_fields):
                if sender == Volunteer:
                    if (instance.user.is_coordinator) \
                        and sync(instance, instance.user.coordinator,
                                 attrs=PROFILES_FIELDS_TO_SYNC):
                        instance.user.coordinator.save()

                if sender == Coordinator:
                    if (instance.user.is_volunteer) \
                        and sync(instance, instance.user.volunteer,
                                 attrs=PROFILES_FIELDS_TO_SYNC):
                        instance.user.volunteer.save()


def update_profile_info(profile, user):
    # Only save if there's been a change,
    # to avoid looping infinitely
    if sync(user, profile):
        profile.save()


def sync(source, target, attrs=USER_FIELDS_TO_SYNC):
    """
    Synchronises attributes of the source object
    to the target object

    Returns whether values have been changed on the target
    during the synchronisation
    """
    changed = False
    for attr in attrs:
        changed = sync_attr(source, target, attr)
    return changed


def sync_attr(source, target, source_attr, target_attr=None):
    """
    Synchronises `source_attr` on the `source` object
    to `target_attr` of the `target` object.

    If no `target_attr` is given, assume the synchronisation
    goes to the same attribute on the target
    """
    if not target_attr:
        target_attr = source_attr
    value = getattr(source, source_attr)
    # Little security to not wipe things
    # When the admin user is created
    if (value and value != getattr(target, target_attr)):
        setattr(target, target_attr, value)
        return True
    return False


def sync_user(source, target, attrs=USER_FIELDS_TO_SYNC):
    """
    Add synchronisation of username to the synchronisation of user
    """
    changed = sync(source, target, attrs)
    return changed or sync_attr(source, target, 'email', 'username')

###
# User status synchronisation for coordiantors
###


# Ideally, if this could be moved in the Coordinator class
# so that the code creating the user with the right permissions
# and the one adjusting their permission was in the same place,
# that would be ideal


@receiver(post_save, sender=Coordinator, dispatch_uid="CoordinatorUpdated")
def transfer_coordinator_status(sender, instance, **kwargs):
    previous_user = instance.previous_user
    new_user = instance.user
    if previous_user:
        previous_user.is_staff = False
        previous_user.is_superuser = False
        previous_user.coordinator = None
        previous_user.save()

    new_user.is_staff = True
    new_user.is_superuser = True
    # No need to set coordinator as it is already set by Django
    new_user.save()


@receiver(post_delete, sender=Coordinator, dispatch_uid="CoordinatorDeleted")
def post_delete_coordinator(sender, instance, **kwargs):
    """
    Automatically delete users if there's no profile attached to them
    or adjust privileges
    """
    # Remove superuser and staff privileges
    # for non-coordinator users
    user = instance.user
    user.is_staff = False
    user.is_superuser = False
    user.coordinator = None
    user.save()

###
# User information coordination
###


@receiver(post_save, sender=User, dispatch_uid="UserSaved")
def post_save_user(sender, instance, created, **kwargs):
    if not created:
        # Need to check before accessing relations
        # as it would throw a NotFoundException
        if (instance.is_volunteer):
            update_profile_info(instance.volunteer, instance)
        if (instance.is_coordinator):
            update_profile_info(instance.coordinator, instance)

        # Get the admin username from the environment.
        admin_user = os.getenv("DJANGO_ADMIN_FIRSTNAME", "admin")

        # Delete users that are no longer coordinators or volunteers, or admin.
        if not (instance.is_coordinator
                or instance.is_volunteer
                or instance.username == admin_user):
            instance.delete()
