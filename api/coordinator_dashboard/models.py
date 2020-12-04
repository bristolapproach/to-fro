from django.db import models


COMMUNICATION_TYPES = (
    ('phone', 'Phone'),
    ('email', 'Email'),
    ('letter', 'Letter')
)

REFERRAL_STATUSES = (
    ('pending', 'Pending'),
    ('complete', 'Complete')
)


class Communication(models.Model):

    added_by = models.ForeignKey(
        'users.Person', on_delete=models.PROTECT,
        related_name='communications_added'
    )
    communication_type = models.CharField(
        max_length=30, choices=COMMUNICATION_TYPES
    )

    resident = models.ForeignKey(
        'users.Resident', on_delete=models.PROTECT,
        related_name='communications'
    )
    actions = models.ManyToManyField('actions.ActionV2')
    referrals = models.ManyToManyField('Referral')

    notes = models.TextField(blank=True, null=True)

    communication_start_datetime = models.DateTimeField()
    communication_end_datetime = models.DateTimeField(blank=True, null=True)

    # skipped: referrer_org (this is on the referral)


class Organisation(models.Model):

    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)

    referral_types = models.ManyToManyField('ReferralType')

    # skipped: phone_secondary, notes, referrals_in, referrals_out, inactive


class ReferralRequirement(models.Model):
    name = models.CharField(max_length=200)


class ReferralType(models.Model):
    name = models.CharField(max_length=200)
    requirements = models.ManyToManyField(ReferralRequirement)


class Referral(models.Model):
    external_referral_id = models.CharField(max_length=80, blank=True, null=True)

    status = models.CharField(
        max_length=30, default='pending', choices=REFERRAL_STATUSES
    )
    referral_type = models.ForeignKey(ReferralType, on_delete=models.PROTECT)
    referral_organisation = models.ForeignKey(
        Organisation, on_delete=models.PROTECT
    )

    notes = models.TextField(blank=True, null=True)

    created_datetime = models.DateTimeField(auto_now_add=True)
    due_datetime = models.DateTimeField(blank=True, null=True)
    completed_datetime = models.DateTimeField(blank=True, null=True)

    # skipped: uploaded_file_url, resident, referral_completed, referral_information

    @property
    def title(self):
        return f"Referral on {self.created_datetime} from {self.referral_organisation.name}"

    def get_admin_detail_url(self):
        return f"/admin/coordinator_dashboard/referral/{self.pk}/change/"
