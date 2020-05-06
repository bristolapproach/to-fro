from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from core.models import Job, Volunteer, JobStatus
from django.core.paginator import Paginator
from django.contrib import messages
from django.views import generic
from django.urls import reverse
from django.db.models import Q
import datetime


LIST_DEFINITIONS = {
    'available': {
        'title': 'Available jobs',
        'heading': 'Available jobs',
        'queryset': lambda volunteer:
            Job.objects.filter(job_status=JobStatus.PENDING)
                       .filter(requester__ward__in=volunteer.wards.all())
                       .filter(help_type__in=volunteer.help_types.all())
                       .order_by('requested_datetime', '-job_priority')
    },
    'completed': {
        'title': 'Completed',
        'heading': 'Heading',
        'queryset': lambda volunteer:
            volunteer.job_set.filter(
                Q(job_status=JobStatus.COMPLETED) | Q(job_status=JobStatus.COULDNT_COMPLETE))
        .order_by('requested_datetime', '-job_priority')
    },
    'mine': {
        'title': 'My tasks',
        'heading': 'Heading',
        'queryset': lambda volunteer:
            volunteer.job_set.exclude(
                Q(job_status=JobStatus.COMPLETED) | Q(job_status=JobStatus.COULDNT_COMPLETE))
        .order_by('requested_datetime', '-job_priority')
    }
}


class JobsListView(generic.ListView):
    template_name = 'tasks/index.html'
    context_object_name = 'jobs'
    list_type = 'available'
    paginate_by = 20

    def get_queryset(self):
        volunteer = self.request.user.volunteer
        return LIST_DEFINITIONS[self.list_type]['queryset'](volunteer)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['current_list_type'] = self.list_type
        context['title'] = LIST_DEFINITIONS[self.list_type]['title']
        context['heading'] = LIST_DEFINITIONS[self.list_type]['heading']
        return context


def back_url(job, volunteer):
    if (job.volunteer != volunteer):
        return reverse('tasks:available')

    if (job.job_status == JobStatus.INTEREST or job.job_status == JobStatus.ASSIGNED):
        return reverse('tasks:index')

    if (job.job_status == JobStatus.COULDNT_COMPLETE or job.job_status == JobStatus.COMPLETED):
        return reverse('tasks:completed')

    return reverse('tasks:available')


def detail(request, task_id):
    volunteer = request.user.volunteer
    job = get_object_or_404(Job, pk=task_id)

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

    context = {
        'job': job,
        'back_url': back_url(job, volunteer),
        'title': "How you can help",
        'heading': job.description,
        'volunteer': volunteer
    }

    return render(request, 'tasks/detail.html', context)


def complete(request, task_id):
    volunteer = request.user.volunteer
    job = get_object_or_404(Job, pk=task_id)

    if job.job_status != JobStatus.ASSIGNED or job.volunteer != volunteer:
        return redirect('tasks:detail', task_id=job.id)

    if request.method == "POST":
        try:
            # the duration field expects seconds, but we ask for an input in hours
            job.time_taken = datetime.timedelta(
                hours=float(request.POST['time_taken']))
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
        'back_url': reverse('tasks:detail', kwargs={'task_id': job.id}),
        'title': 'How did it go?',
        'heading': 'How did it go?',
    }

    return render(request, 'tasks/complete.html', context)
