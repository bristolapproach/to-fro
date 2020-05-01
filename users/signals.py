from users.models import UserRole, Coordinator, Requester, Volunteer
from django.db.models.signals import post_save


# Register function to trigger after saving a Coordinator.
def save_coordinator(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.COORDINATOR
        instance.save()
post_save.connect(save_coordinator, Coordinator, weak=False, dispatch_uid="CoordinatorSignal")


# Register function to trigger after saving a Requester.
def save_requester(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.REQUESTER
        instance.save()

post_save.connect(save_requester, Requester, weak=False, dispatch_uid="RequesterSignal")

# Register function to trigger after saving a Volunteer.
def save_volunteer(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.VOLUNTEER
        instance.save()
post_save.connect(save_volunteer, Volunteer, weak=False, dispatch_uid="VolunteerSignal")
