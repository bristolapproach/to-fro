from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from categories.models import HelpType, Ward
from users.models import Volunteer, UserProfileMixin

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


@receiver(post_delete, sender=UserProfileMixin, dispatch_uid="UserProfileDeleted")
def post_delete_user_profile(sender, instance, **kwargs):
    """
    Automatically delete users if there's no profile attached to them
    """
    logger.debug(sender)
