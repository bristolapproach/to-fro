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

FIELDS_TO_SYNC = (
    'first_name',
    'last_name',
    'email'
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
        if some(FIELDS_TO_SYNC, lambda field_name: field_name in changed_fields):
            # Always save the user, to ensure changes
            # get propagated to the other profile
            sync(instance, instance.user)
            instance.user.save()


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


def sync(source, target, attrs=FIELDS_TO_SYNC):
    """
    Synchronises attributes of the source object
    to the target object

    Returns whether values have been changed on the target
    during the synchronisation
    """
    changed = False
    for attr in FIELDS_TO_SYNC:
        value = getattr(source, attr)
        # Little security to not wipe things
        # When the admin user is created
        logger.debug('Syncing %s: %s (existing %s)',
                     attr, value, getattr(target, attr))
        if (value and value != getattr(target, attr)):
            logger.debug('Setting %s', attr)
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
