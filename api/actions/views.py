from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from actions.models import Action, ActionStatus
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from django.db.models import Q
import datetime


LIST_DEFINITIONS = {
    'available': {
        'title': 'Available actions',
        'heading': 'Available actions',
        'queryset': lambda volunteer:
            Action.objects.filter(action_status=ActionStatus.PENDING)
        .filter(resident__ward__in=volunteer.wards.all())
        .filter(help_type__in=volunteer.help_types.all())
        .order_by('requested_datetime', '-action_priority')
    },
    'completed': {
        'title': 'Completed',
        'heading': 'Completed',
        'queryset': lambda volunteer:
            volunteer.action_set.filter(
                Q(action_status=ActionStatus.COMPLETED) | Q(action_status=ActionStatus.COULDNT_COMPLETE))
        .order_by('requested_datetime', '-action_priority')
    },
    'mine': {
        'title': 'My actions',
        'heading': 'My actions',
        'queryset': lambda volunteer:
            volunteer.action_set.exclude(
                Q(action_status=ActionStatus.COMPLETED) | Q(action_status=ActionStatus.COULDNT_COMPLETE))
            .order_by('requested_datetime', '-action_priority')
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
    if (action.volunteer != volunteer):
        return reverse('actions:available')

    if (action.action_status == ActionStatus.INTEREST or action.action_status == ActionStatus.ASSIGNED):
        return reverse('actions:index')

    if (action.action_status == ActionStatus.COULDNT_COMPLETE or action.action_status == ActionStatus.COMPLETED):
        return reverse('actions:completed')

    return reverse('actions:available')


def detail(request, action_id):
    volunteer = request.user.volunteer
    action = get_object_or_404(Action, pk=action_id)

    if request.method == "POST":
        if (action.action_status != ActionStatus.PENDING):
            messages.error(
                request, 'Thanks, but someone has already volunteered to help')
        else:
            action.volunteer = volunteer
            action.action_status = ActionStatus.INTEREST
            action.save()
            messages.success(request, 'Thanks for volunteering!')
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

    if action.action_status != ActionStatus.ASSIGNED or action.volunteer != volunteer:
        return redirect('actions:detail', action_id=action.id)

    if request.method == "POST":
        try:
            # the duration field expects seconds, but we ask for an input in hours
            action.time_taken = datetime.timedelta(
                hours=float(request.POST['time_taken']))
            action.notes = request.POST['notes']
            if (request.POST['outcome'] == 'ok'):
                action.action_status = ActionStatus.COMPLETED
                action.save()
                messages.success(request, 'Nice work! Thanks for helping out!')
            else:
                action.action_status = ActionStatus.COULDNT_COMPLETE
                action.save()
                messages.success(
                    request, 'Thanks for helping out! Sorry it did not all go smoothly.')
            return redirect('actions:detail', action_id=action.id)
        except:
            messages.error(
                request, 'Sorry, we could not save your information. Please double check the form.')

    context = {
        'action': action,
        'back_url': reverse('actions:detail', kwargs={'action_id': action.id}),
        'title': 'How did it go?',
        'heading': 'How did it go?',
    }

    return render(request, 'actions/complete.html', context)