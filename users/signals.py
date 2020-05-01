from users.models import UserRole, Requester, Volunteer
from django.db.models.signals import post_save


# Register function to trigger after saving a Requester.
def save_requester(sender, instance, **kwargs):
    print("Requester saved")
    if instance.role is None:
        instance.role = UserRole.REQUESTER
        instance.save()
post_save.connect(save_requester, Requester, weak=False, dispatch_uid="RequesterSignal")

# Register function to trigger after saving a Volunteer.
def save_volunteer(sender, instance, **kwargs):
    print("Volunteer saved")
    if instance.role is None:
        instance.role = UserRole.VOLUNTEER
        instance.save()
post_save.connect(save_volunteer, Volunteer, weak=False, dispatch_uid="VolunteerSignal")
