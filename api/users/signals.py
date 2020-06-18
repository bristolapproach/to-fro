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
            if some(USER_FIELDS_TO_SYNC, lambda field_name: field_name in changed_fields) and sync(instance, instance.user):
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
        value = getattr(source, attr)
        # Little security to not wipe things
        # When the admin user is created
        if (value and value != getattr(target, attr)):
            changed = True
            setattr(target, attr, value)
    return changed


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
