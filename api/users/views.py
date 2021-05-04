from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from rest_framework import mixins
from .models import Resident, Volunteer, Coordinator
from .serializers import  ResidentSerializer, VolunteerSerializer, CoordinatorSerializer
from core.views import BaseToFroViewSet

from users.forms import UserSettingsForm

class ResidentViewSet(mixins.UpdateModelMixin, BaseToFroViewSet):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer


class VolunteerViewSet(BaseToFroViewSet):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer


class CoordinatorViewSet(BaseToFroViewSet):
    queryset = Coordinator.objects.all()
    serializer_class = CoordinatorSerializer


class UserSettingsView(FormView):
    template_name = 'users/user_settings.html'
    form_class = UserSettingsForm

    volunteer_fields = [
        ('user_email', 'email'),
        ('user_phone', 'phone'),
        ('user_phone_secondary', 'phone_secondary'),
        ('daily_digest_optin',  'daily_digest_optin'),
        ('weekly_digest_optin', 'weekly_digest_optin'),
    ]

    @classmethod
    def _update_volunteer(cls, volunteer_obj, form_data):
        volunteer_updated = False

        for form_field, volunteer_field in cls.volunteer_fields:
            field_value = form_data[form_field]
            if field_value != getattr(volunteer_obj, volunteer_field):
                setattr(volunteer_obj, volunteer_field, field_value)
                volunteer_updated = True

        if volunteer_updated:
            volunteer_obj.save()

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = self.request.user

        if form_data.get('new_password'):
            user.set_password(form_data['new_password'])
            user.save()

        self._update_volunteer(user.volunteer, form_data)

        messages.success(self.request, "You've updated your settings")

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(UserSettingsView, self).get_form_kwargs()
        kwargs['user'] = user = self.request.user

        if 'initial' not in kwargs:
            kwargs['initial'] = {}

        kwargs['initial'].update({
            form_field: getattr(user.volunteer, volunteer_field)
            for (form_field, volunteer_field) in self.volunteer_fields
        })

        return kwargs

    def get_success_url(self):
        return reverse('user-settings')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user, 'title': 'Account Settings', 'back_url': reverse('actions:available')
        })
        return context

