from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q
from django.views import generic
from django.core.paginator import Paginator
from core.models import Job, Volunteer, JobStatus
import datetime

LIST_DEFINITIONS = {
    'available': {
        'title': 'Available jobs',
        'heading': 'Available jobs',
        'queryset': lambda volunteer:
            Job.objects.filter(job_status=JobStatus.PENDING) \
                       .filter(requester__ward__in=volunteer.wards.all()) \
                       .filter(help_type__in=volunteer.help_types.all())
    },
    'completed': {
        'title': 'Completed',
        'heading': 'Heading',
        'queryset': lambda volunteer:
            volunteer.job_set.filter(
                Q(job_status=JobStatus.COMPLETED) | Q(job_status=JobStatus.COULDNT_COMPLETE))
    },
    'mine': {
        'title': 'My tasks',
        'heading': 'Heading',
        'queryset': lambda volunteer:
            volunteer.job_set.exclude(
                Q(job_status=JobStatus.COMPLETED) | Q(job_status=JobStatus.COULDNT_COMPLETE))
    }
}


class JobsListView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'jobs'
    paginate_by = 20
    list_type = 'available'

    def get_queryset(self):
        volunteer = Volunteer.objects.first()
        return LIST_DEFINITIONS[self.list_type]['queryset'](volunteer)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['current_list_type'] = self.list_type
        context['title'] = LIST_DEFINITIONS[self.list_type]['title']
        context['heading'] = LIST_DEFINITIONS[self.list_type]['heading']
        return context


def detail(request, task_id):
    volunteer = Volunteer.objects.first()
    job = get_object_or_404(Job, pk=task_id)
    context = {
        'job': job,
        'backUrl': '.',
        'title': "How you can help",
        'heading': job.description,
        'volunteer': volunteer
    }

    if request.method == "POST":
        if (job.job_status != JobStatus.PENDING):
            messages.error(
                request, 'Thanks, but someone has already volunteered to help')
        else:
            job.volunteer = volunteer
            job.job_status = JobStatus.INTEREST
            job.save()
            messages.success(request, 'Thanks for volunteering!')
        return redirect('tasks:detail', task_id=job.id)

    return render(request, 'tasks/detail.html', context)


def complete(request, task_id):
    volunteer = Volunteer.objects.first()
    job = get_object_or_404(Job, pk=task_id)

    if job.job_status != JobStatus.ASSIGNED or job.volunteer != volunteer:
        return redirect('tasks:detail', task_id=job.id)

    if request.method == "POST":
        try:
            # the duration field expects seconds, but we ask for an input in hours
            job.timeTaken = datetime.timedelta(
                hours=float(request.POST['timeTaken']))
            job.notes = request.POST['notes']
            if (request.POST['outcome'] == 'ok'):
                job.job_status = JobStatus.COMPLETED
                job.save()
                messages.success(request, 'Nice work! Thanks for helping out!')
            else:
                job.job_status = JobStatus.COULDNT_COMPLETE
                job.save()
                messages.success(
                    request, 'Thanks for helping out! Sorry it did not all go smoothly.')
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
