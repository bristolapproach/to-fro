import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from core.models import Job, Helper, JobStatus
from django.views import generic

LIST_DEFINITIONS = {
    'available': {
        'title': 'Available jobs',
        'heading': 'Available jobs',
        'queryset': lambda helper:
            Job.objects.filter(
                job_status__name='pending_help').filter(requester__ward__in=helper.wards.all()).filter(help_type__in=helper.help_types.all())
    },
    'completed': {
        'title': 'Completed',
        'heading': 'Heading',
        'queryset': lambda helper:
            helper.job_set.filter(
                Q(job_status__name='completed') | Q(job_status__name='couldnt_complete'))
    },
    'mine': {
        'title': 'My tasks',
        'heading': 'Heading',
        'queryset': lambda helper:
            helper.job_set.exclude(
                Q(job_status__name='completed') | Q(job_status__name='couldnt_complete'))
    }
}


class JobsListView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'jobs'
    paginate_by = 20
    list_type = 'available'

    def get_queryset(self):
        helper = Helper.objects.first()
        return LIST_DEFINITIONS[self.list_type]['queryset'](helper)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['current_list'] = self.list_type
        context['title'] = LIST_DEFINITIONS[self.list_type]['title']
        context['heading'] = LIST_DEFINITIONS[self.list_type]['heading']
        return context


def detail(request, task_id):
    helper = Helper.objects.first()
    job = get_object_or_404(Job, pk=task_id)
    context = {
        'job': job,
        'backUrl': '.',
        'title': "How you can help",
        'heading': job.description,
        'helper': helper
    }

    if request.method == "POST":
        if (job.job_status.name != 'pending_help'):
            messages.error(
                request, 'Thanks, but someone has already volunteered to help')
        else:
            job.helper = helper
            job.job_status = JobStatus.objects.get(name='helper_interest')
            job.save()
            messages.success(request, 'Thanks for volunteering!')
        return redirect('tasks:detail', task_id=job.id)

    return render(request, 'tasks/detail.html', context)


def complete(request, task_id):
    helper = Helper.objects.first()
    job = get_object_or_404(Job, pk=task_id)

    if job.job_status.name != 'helper_assigned' or job.helper != helper:
        return redirect('tasks:detail', task_id=job.id)

    if request.method == "POST":
        try:
            # the duration field expects seconds, but we ask for an input in hours
            job.timeTaken = datetime.timedelta(
                hours=float(request.POST['timeTaken']))
            job.notes = request.POST['notes']
            if (request.POST['outcome'] == 'ok'):
                job.job_status = JobStatus.objects.get(name='completed')
                job.save()
                messages.success(request, 'Nice work! Thanks for helping out!')
            else:
                job.job_status = JobStatus.objects.get(name='couldnt_complete')
                job.save()
                messages.success(
                    request, 'Thanks for helping out! Sorry it did not all go smoothly')
            return redirect('tasks:detail', task_id=job.id)
        except:
            messages.error(
                request, 'Sorry, we could not save your information. Please double check the form.')

    context = {
        'job': job,
        'backUrl': '..',
        'title': 'How did it go?',
        'heading': 'How did it go?',
    }

    return render(request, 'tasks/complete.html', context)
