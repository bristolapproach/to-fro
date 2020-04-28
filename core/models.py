from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_number_primary = models.CharField(
        max_length=15, null=True, help_text="Main phone number for the user.")
    phone_number_secondary = models.CharField(
        max_length=15, null=True, help_text="Secondary phone number for the user.", blank=True)
    email_primary = models.CharField(
        max_length=50, null=True, help_text="Main email for the user.", blank=True)
    email_secondary = models.CharField(
        max_length=50, null=True, help_text="Secondary email for the user.", blank=True)
    notes = models.CharField(max_length=500, null=True,
                             help_text="Any other notes?", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"


class EventType(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"EventType: {self.name}"


class Event(models.Model):
    user = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, help_text="Who triggered the event?")
    event_type = models.ForeignKey(
        EventType, null=True, on_delete=models.PROTECT, help_text="What was the event?")
    datetime = models.DateTimeField(null=True, help_text="When was the event?")

    def __str__(self):
        return f"Event: {self.id}"


class Relationship(models.Model):
    user_1 = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name="user_1")
    user_2 = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name="user_2")
    created_datetime = models.DateTimeField(
        null=True, help_text="When did they first make contact?")

    def __str__(self):
        return f"Relationship: {self.id} (between {self.user_1} and {self.user_2}"


class Ward(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class HelpType(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f"{self.name}"


class Requester(User):
    user_type = models.CharField(
        max_length=20, null=True, default="requester", blank=True)
    address_line_1 = models.CharField(
        max_length=100, null=True, help_text="First line of their address.")
    address_line_2 = models.CharField(
        max_length=100, null=True, help_text="Second line of their address.", blank=True)
    address_line_3 = models.CharField(
        max_length=100, null=True, help_text="Third line of their address.", blank=True)
    postcode = models.CharField(
        max_length=100, null=True, help_text="Address postcode.")
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT,
                             null=True, help_text="Which ward is this address in")
    internet_access = models.BooleanField(
        null=True, help_text="Does this person have internet access?")
    smart_device = models.BooleanField(
        null=True, help_text="Does this person have a smart device?")
    confident_online_shopping = models.BooleanField(
        null=True, help_text="Is this person confident online shopping?")
    confident_online_comms = models.BooleanField(
        null=True, help_text="Is this person confident communicating online?")
    shielded = models.BooleanField(
        null=True, help_text="Is this person sheilded?")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"


class Helper(User):
    user_type = models.CharField(max_length=20, null=True, default="helper")
    dbs_number = models.CharField(
        max_length=12, null=True, blank=True, help_text="The user's DBS certificate number, if they have one.")
    access_to_car = models.BooleanField(
        null=True, help_text="Does this person have access to a car?")
    driving_license = models.BooleanField(
        null=True, help_text="Does this person have a driving license?")
    ts_and_cs_confirmed = models.BooleanField(
        null=True, help_text="Has this person agreed to the terms and conditions?")
    health_checklist_received = models.BooleanField(
        null=True, help_text="Have we received their health checklist?")
    key_worker = models.BooleanField(
        null=True, help_text="Have we received their key worker letter?")
    id_received = models.BooleanField(
        null=True, help_text="Have we received a copy of their ID?")
    wards = models.ManyToManyField(Ward, related_name="helpers")
    help_types = models.ManyToManyField(HelpType, related_name="helpers")
    reference_details = models.CharField(max_length=250, null=True, blank=True)
    available_mon_morning = models.BooleanField(null=True, default=False)
    available_mon_afternoon = models.BooleanField(null=True, default=False)
    available_mon_evening = models.BooleanField(null=True, default=False)
    available_tues_morning = models.BooleanField(null=True, default=False)
    available_tues_afternoon = models.BooleanField(null=True, default=False)
    available_tues_evening = models.BooleanField(null=True, default=False)
    available_wed_morning = models.BooleanField(null=True, default=False)
    available_wed_afternoon = models.BooleanField(null=True, default=False)
    available_wed_evening = models.BooleanField(null=True, default=False)
    available_thur_morning = models.BooleanField(null=True, default=False)
    available_thur_afternoon = models.BooleanField(null=True, default=False)
    available_thur_evening = models.BooleanField(null=True, default=False)
    available_fri_morning = models.BooleanField(null=True, default=False)
    available_fri_afternoon = models.BooleanField(null=True, default=False)
    available_fri_evening = models.BooleanField(null=True, default=False)
    available_sat_morning = models.BooleanField(null=True, default=False)
    available_sat_afternoon = models.BooleanField(null=True, default=False)
    available_sat_evening = models.BooleanField(null=True, default=False)
    available_sun_morning = models.BooleanField(null=True, default=False)
    available_sun_afternoon = models.BooleanField(null=True, default=False)
    available_sun_evening = models.BooleanField(null=True, default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.id})"


class JobPriority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class JobStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Job(models.Model):
    added_by = models.CharField(
        max_length=100, null=True, help_text="What's your name?")
    designated_coordinator = models.CharField(
        max_length=100, null=True, help_text="Who will mediate this help?")
    call_datetime = models.DateTimeField(
        null=True, help_text="What time did you receive the call about the help requested?")
    call_duration = models.DurationField(
        null=True, blank=True, help_text="How long was the call?")
    requester = models.ForeignKey(
        Requester, on_delete=models.PROTECT, null=True, help_text="Who made the request?")
    requested_datetime = models.DateTimeField(
        null=True, help_text="When do they need the help by?")
    helper = models.ForeignKey(
        Helper, on_delete=models.PROTECT, null=True, blank=True, help_text="Who will help?")
    job_status = models.ForeignKey(
        JobStatus, on_delete=models.PROTECT, null=True, help_text="What's the status of the help?")
    job_priority = models.ForeignKey(
        JobPriority, on_delete=models.PROTECT, null=True, help_text="What's the priority of the help?")
    timeTaken = models.DurationField(
        null=True, help_text="How long did it take to help?")
    notes = models.TextField(max_length=500, null=True, blank=True, 
                             help_text="Any other notes?")
    public_description = models.TextField(
        max_length=500, null=True, help_text="Text that gets displayed to helpers.")
    private_description = models.TextField(
        null=True, blank=True, help_text="Text that'll only get displayed to the helpers after they did the job")
    help_type = models.ForeignKey(
        HelpType, on_delete=models.PROTECT, null=True, help_text="Which kind of help is needed")

    @property
    def ward(self):
        return self.requester.ward

    @property
    def description(self):
        return f"Help with {self.help_type} around {self.ward}"

    @property
    def descriptionWithDate(self):
        return f"{self.description} by {self.requested_datetime.strftime('%d %b')}"

    def __str__(self):
        return f"Job: {self.id}"

class Notification(models.Model):
    job = models.ForeignKey(Job, null=True, on_delete=models.PROTECT, help_text="The job the notification is about.")
    subject = models.CharField(
        max_length=100, null=True, help_text="The notification subject.")
    message = models.TextField(
        max_length=1000, null=True, help_text="What's your name?")
    delivered = models.BooleanField(default=False, help_text="This field is updated automatically.")
    sent_by = models.CharField(max_length=50, help_text="Who's sending the notification?")
    recipients = models.ManyToManyField(User, related_name='notificationrecipient', default=[], help_text="This field is updated automatically.")
    created_date_time = models.DateTimeField(null=True, help_text="This field is updated automatically.")
    delivered_date_time = models.DateTimeField(null=True, help_text="This field is updated automatically.")

