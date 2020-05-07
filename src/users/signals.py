from users.models import UserRole, Coordinator, Resident, Volunteer
from django.db.models.signals import post_save


# Register function to trigger after saving a Coordinator.
def save_coordinator(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.COORDINATOR
        instance.save()


post_save.connect(save_coordinator, Coordinator, weak=False,
                  dispatch_uid="CoordinatorSignal")


# Register function to trigger after saving a Resident.
def save_resident(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.RESIDENT
        instance.save()


post_save.connect(save_resident, Resident, weak=False,
                  dispatch_uid="ResidentSignal")

# Register function to trigger after saving a Volunteer.


def save_volunteer(sender, instance, **kwargs):
    if instance.role is None or instance.role == '':
        instance.role = UserRole.VOLUNTEER
        instance.save()


post_save.connect(save_volunteer, Volunteer, weak=False,
                  dispatch_uid="VolunteerSignal")
