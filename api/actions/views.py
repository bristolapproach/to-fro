from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from actions.models import Action, ActionStatus
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from .forms import ActionFeedbackForm


LIST_DEFINITIONS = {
    'available': {
        'title': 'Available actions',
        'heading': 'Available actions',
        'queryset': lambda volunteer:
            volunteer.available_actions.order_by(
                'requested_datetime', '-action_priority')
    },
    'completed': {
        'title': 'Completed',
        'heading': 'Completed',
        'queryset': lambda volunteer:
            volunteer.completed_actions.order_by(
                'requested_datetime', '-action_priority')
    },
    'ongoing': {
        'title': 'Ongoing',
        'heading': 'Ongoing',
        'queryset': lambda volunteer:
            volunteer.ongoing_actions.order_by(
                'requested_datetime', '-action_priority'
            )
    },
    'mine': {
        'title': 'My actions',
        'heading': 'My actions',
        'queryset': lambda volunteer:
        volunteer.upcoming_actions.order_by(
            'requested_datetime', '-action_priority')
    }
}


class ActionsListView(generic.ListView):
    template_name = 'actions/index.html'
    context_object_name = 'actions'
    list_type = 'available'
    paginate_by = 20

    def get_queryset(self):
        volunteer = self.request.user.volunteer
        # Avoid N+1 queries when rendering the list of actions
        return LIST_DEFINITIONS[self.list_type]['queryset'](volunteer).select_related('help_type', 'resident', 'resident__ward')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['current_list_type'] = self.list_type
        context['title'] = LIST_DEFINITIONS[self.list_type]['title']
        context['heading'] = LIST_DEFINITIONS[self.list_type]['heading']
        return context


def back_url(action, volunteer):
    if (action.assigned_volunteer != volunteer):
        return reverse('actions:available')

    if (action.action_status == ActionStatus.INTEREST or action.action_status == ActionStatus.ASSIGNED):
        return reverse('actions:index')

    if (action.action_status == ActionStatus.ONGOING):
        return reverse('actions:ongoing')

    if (action.action_status == ActionStatus.COULDNT_COMPLETE or action.action_status == ActionStatus.COMPLETED):
        return reverse('actions:completed')

    return reverse('actions:available')


def detail(request, action_id):
    volunteer = request.user.volunteer
    action = get_object_or_404(Action, pk=action_id)

    if request.method == "POST":
        if request.POST.get('_action') == 'contact':
            action.register_volunteer_contact()
            action.save()
        else:
            # Check if the action still needs volunteers to register interest.
            if action.action_status == ActionStatus.PENDING \
                    or action.action_status == ActionStatus.INTEREST:

                # If so, add the volunteer.
                if volunteer not in action.interested_volunteers.all():
                    action.interested_volunteers.add(volunteer)
                    action.action_status = ActionStatus.INTEREST
                    action.save()
                messages.success(request, 'Thanks for volunteering!')
            else:
                messages.error(
                    request, 'Thanks, but someone has already volunteered to help')
        return redirect('actions:detail', action_id=action.id)

    context = {
        'action': action,
        'back_url': back_url(action, volunteer),
        'title': "How you can help",
        'heading': action.description,
        'volunteer': volunteer
    }

    return render(request, 'actions/detail.html', context)


def complete(request, action_id):
    volunteer = request.user.volunteer
    action = get_object_or_404(Action, pk=action_id)

    if action.action_status != ActionStatus.ASSIGNED or action.assigned_volunteer != volunteer:
        return redirect('actions:detail', action_id=action.id)

    form = ActionFeedbackForm(request.POST or None, instance=action)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Nice work! Thanks for helping out!')
        return redirect('actions:detail', action_id=action.id)

    context = {
        'action': action,
        'back_url': reverse('actions:detail', kwargs={'action_id': action.id}),
        'title': 'How did it go?',
        'heading': 'How did it go?',
        'form': form
    }

    return render(request, 'actions/complete.html', context)
