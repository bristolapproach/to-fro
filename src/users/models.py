from django.db import models
from django.contrib.auth.models import User

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Ward(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class HelpType(models.Model):
    name = models.CharField(max_length=50, null=True)
    private_description_template = models.TextField(
        null=True, blank=True, help_text="Private description will be pre-filled with this text when picking this type of help for a Job")
    public_description_template = models.TextField(
        null=True, blank=True, help_text="Public description will be pre-filled with this text when picking this type of help for a Job")

    def __str__(self):
        return f"{self.name}"


class UserRole:
    '''Constants used in the User class.'''
    COORDINATOR, RESIDENT, VOLUNTEER = '1', '2', '3'
    ROLES = [
        (COORDINATOR, "Coordinator"),
        (RESIDENT, "Resident"),
        (VOLUNTEER, "Volunteer")
    ]


class Person(models.Model):
    '''Shared profile attributes
    '''

    # Custom User attributes.
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=15, null=True, blank=True, help_text="Main phone number for the user.")
    phone_secondary = models.CharField(
        max_length=15, null=True, blank=True, help_text="Secondary phone number for the user.")
    email = models.CharField(max_length=50, null=True,
                             blank=True, help_text="Main email for the user.")
    email_secondary = models.CharField(
        max_length=50, null=True, blank=True, help_text="Secondary email for the user.")
    notes = models.TextField(null=True,
                             blank=True, help_text="Any other notes?")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class UserProfileMixin(models.Model):
    """
    An abstract mixin to add the link to auth.User

    This ensures that each kind of profile has their own
    attribute, enforcing that a user can have only one
    profile of each kind

    Note: The addition of the OneToOne field is left to the
    extending class, so that a custom related_name can be set for the relation
    """
    user_is_staff = False

    class Meta:
        abstract = True

    user_without_account = models.BooleanField(
        null=False, default=False, blank=True
    )

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (not self.user_without_account and not bool(self.user)):
            self.create_user()
        if (self.user_without_account and bool(self.user)):
            self.user = None
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def create_user(self):
        user = User(username=self.email, email=self.email)
        user.is_staff = self.user_is_staff
        setattr(user, self.profile_type, self)
        user.save()


class Resident(Person):
    address_line_1 = models.CharField(
        max_length=100, help_text="First line of their address.")
    address_line_2 = models.CharField(
        max_length=100, null=True, blank=True, help_text="Second line of their address.")
    address_line_3 = models.CharField(
        max_length=100, null=True, blank=True, help_text="Third line of their address.")
    postcode = models.CharField(max_length=10, help_text="Address postcode.")
    ward = models.ForeignKey(Ward, null=True, on_delete=models.PROTECT,
                             help_text="The ward containing the above address.")
    internet_access = models.BooleanField(
        default=False, help_text="Does this person have internet access?")
    smart_device = models.BooleanField(
        default=False, help_text="Does this person have a smart device?")
    confident_online_shopping = models.BooleanField(
        default=False, help_text="Is this person confident online shopping?")
    confident_online_comms = models.BooleanField(
        default=False, help_text="Is this person confident communicating online?")
    shielded = models.BooleanField(
        default=False, help_text="Is this person shielded?")


class Volunteer(UserProfileMixin, Person):
    dbs_number = models.CharField(max_length=12, null=True, blank=True,
                                  help_text="The user's DBS certificate number, if they have one.")
    access_to_car = models.BooleanField(
        null=True, verbose_name="Has access to car")
    driving_license = models.BooleanField(
        null=True, verbose_name="Has a driving license")
    ts_and_cs_confirmed = models.BooleanField(
        null=True, verbose_name="Has agreed to terms and conditions")
    health_checklist_received = models.BooleanField(
        null=True, verbose_name="Has received their health checklist")
    key_worker = models.BooleanField(
        null=True, verbose_name="Has received key worker letter from council")
    id_received = models.BooleanField(
        null=True, verbose_name="Has sent a copy of their ID")
    wards = models.ManyToManyField(
        Ward, blank=True, related_name="volunteer_wards")
    help_types = models.ManyToManyField(
        HelpType, related_name="volunteer_help_types")
    reference_details = models.CharField(max_length=250, null=True, blank=True)
    available_mon_morning = models.BooleanField(
        default=False, verbose_name="Monday morning")
    available_mon_afternoon = models.BooleanField(
        default=False, verbose_name="Monday afternoon")
    available_mon_evening = models.BooleanField(
        default=False, verbose_name="Monday evening")
    available_tues_morning = models.BooleanField(
        default=False, verbose_name="Tuesday morning")
    available_tues_afternoon = models.BooleanField(
        default=False, verbose_name="Tuesday afternoon")
    available_tues_evening = models.BooleanField(
        default=False, verbose_name="Tuesday evening")
    available_wed_morning = models.BooleanField(
        default=False, verbose_name="Wednesday morning")
    available_wed_afternoon = models.BooleanField(
        default=False, verbose_name="Wednesday afternoon")
    available_wed_evening = models.BooleanField(
        default=False, verbose_name="Wednesday evening")
    available_thur_morning = models.BooleanField(
        default=False, verbose_name="Thursday morning")
    available_thur_afternoon = models.BooleanField(
        default=False, verbose_name="Thursday afternoon")
    available_thur_evening = models.BooleanField(
        default=False, verbose_name="Thursday evening")
    available_fri_morning = models.BooleanField(
        default=False, verbose_name="Friday morning")
    available_fri_afternoon = models.BooleanField(
        default=False, verbose_name="Friday afternoon")
    available_fri_evening = models.BooleanField(
        default=False, verbose_name="Friday evening")
    available_sat_morning = models.BooleanField(
        default=False, verbose_name="Saturday morning")
    available_sat_afternoon = models.BooleanField(
        default=False, verbose_name="Saturday afternoon")
    available_sat_evening = models.BooleanField(
        default=False, verbose_name="Saturday evening")
    available_sun_morning = models.BooleanField(
        default=False, verbose_name="Sunday morning")
    available_sun_afternoon = models.BooleanField(
        default=False, verbose_name="Sunday afternoon")
    available_sun_evening = models.BooleanField(
        default=False, verbose_name="Sunday evening")

    profile_type = 'volunteer'
    related_name = 'volunteer'
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name=related_name)


class Coordinator(UserProfileMixin, Person):
    user_is_staff = True
    related_name = 'coordinator'
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name=related_name)
    pass


# class Relationship(models.Model):
#     user_1 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_1")
#     user_2 = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_2")
#     created_datetime = models.DateTimeField(default=timezone.now, help_text="When did they first make contact?")

#     def __str__(self):
#         return f"{self.id}: {self.user_1} and {self.user_2}"
