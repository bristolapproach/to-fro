import datetime

from django.core.exceptions import SuspiciousOperation
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from actions.models import ActionV2, ActionOccurrenceVolunteerAssignment, ActionOccurrence
from coordinator_dashboard.forms import AddActionForm
from coordinator_dashboard.models import Referral
from users.models import Resident


def coordinator_dashboard_view(request):
    pass
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    three_days_time = yesterday + datetime.timedelta(days=4)

    # or:                               assigned_volunteers__count < num_required_volunteers)
    unassigned_actions = ActionV2.objects.filter(assigned_volunteers__count=0)

    unassigned_actions = ActionOccurrence.objects.filter(

    )

    # or:                                   completed_datetime__isnull=True?
    unactioned_referrals = Referral.objects.filter(status='pending')

    contact_overdue = ActionOccurrenceVolunteerAssignment.objects.filter(
        status='assigned',
        action__due_datetime__date__gte=yesterday,
        action__due_datetime__date__lte=three_days_time
    )

    feedback_overdue = ActionOccurrenceVolunteerAssignment.objects.filter(
        status='contact_made',
        action__due_datetime__date__gte=yesterday,
        action__due_datetime__date__lte=three_days_time
    )

    context = {
        'unassigned_actions': unassigned_actions,
        'unactioned_referrals': unactioned_referrals,
        'contact_overdue': contact_overdue,
        'feedback_overdue': feedback_overdue
    }
    return render(request, 'coordinator_dashboard/dashboard_index.html', context)


def select_resident_view(request):
    if request.method == 'POST':
        resident_pk = request.POST.get('resident_pk')
        if not resident_pk:
            return HttpResponseBadRequest('missing resident_pk')

        request.session['selected_resident_pk'] = resident_pk
        return redirect('select-next-step')

    context = {
        'residents': Resident.objects.all()
    }
    return render(request, 'coordinator_dashboard/select_resident.html', context)


def select_next_step_view(request):

    resident_pk = request.session.get('selected_resident_pk')
    if not resident_pk:
        return redirect('select-resident')

    now = datetime.datetime.now()
    week_ago = now - datetime.timedelta(days=7)

    resident = get_object_or_404(Resident, pk=resident_pk)

    recent_actions = ActionV2.objects.filter(resident=resident, created_datetime__gt=week_ago).exclude(action_status='completed').order_by('-created_datetime')

    recent_referrals = Referral.objects.all().order_by('-created_datetime')

    context = {
        'resident': resident,
        'recent_actions': recent_actions[:7],
        'recent_referrals': recent_referrals[:7]
    }
    return render(request, 'coordinator_dashboard/select_next_step.html', context)


class AddActionView(FormView):
    template_name = 'coordinator_dashboard/add_action.html'
    form_class = AddActionForm

    '''
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
    '''

    def form_valid(self, form):
        data = form.cleaned_data
        new_action = ActionV2.objects.create(
            resident=data['resident'],
            help_type=data['help_type'],
            due_datetime=data['due_datetime'],
            num_volunteers_needed=data['num_volunteers_needed'],
            action_priority=data['action_priority'],
            public_description=data['public_description'] or None,
            private_description=data['private_description'] or None
        )
        new_action.requirements.add(*data['requirements'])

        messages.success(self.request, f"You've added a new action {new_action.pk}")
        return super().form_valid(form)

    def get_form_kwargs(self):
        resident_pk = self.request.session.get('selected_resident_pk')
        if not resident_pk:
            raise SuspiciousOperation('Missing selected_resident_pk')

        kwargs = super(AddActionView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if 'initial' not in kwargs:
            kwargs['initial'] = {}

        kwargs['initial']['resident'] = resident_pk
        return kwargs

    def get_success_url(self):
        return reverse('select-next-step')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user, 'title': 'Add action'
        })
        return context
