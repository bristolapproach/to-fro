from django.contrib import admin

from .models import Communication, Organisation, ReferralRequirement, ReferralType, Referral


admin.site.register(Communication)
admin.site.register(Organisation)
admin.site.register(Referral)
admin.site.register(ReferralType)
admin.site.register(ReferralRequirement)
