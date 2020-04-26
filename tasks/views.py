import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from core.models import Job, Helper


def index(request):
    helper = Helper.objects.get()
    jobs = Job.objects.filter(Q(helper=helper)).exclude(
        Q(job_status__name='completed') | Q(job_status__name='couldnt_complete'))
    context = {
        'currentListType': 'mine',
        'title': 'My jobs',
        'heading': 'My jobs',
        'jobs': jobs
    }
    return render(request, 'tasks/index.html', context)


def available(request):
    jobs = Job.objects.filter(helper__isnull=True)
    context = {
        'currentListType': 'available',
        'title': 'Available jobs',
        'heading': 'Available jobs',
        'jobs': jobs
    }
    return render(request, 'tasks/index.html', context)


def completed(request):
    helper = Helper.objects.get()
    jobs = Job.objects.filter(Q(helper=helper)).filter(
        Q(job_status__name='completed') | Q(job_status__name='couldnt_complete'))
    context = {
        'currentListType': 'completed',
        'title': 'Completed jobs',
        'heading': 'Completed jobs',
        'jobs': jobs
    }
    return render(request, 'tasks/index.html', context)


def detail(request, task_id):
    job = get_object_or_404(Job, pk=task_id)
    context = {
        'job': job,
        'backUrl': '.',
        'title': "How you can help",
        'heading': job.description
    }

    if request.method == "POST":
        messages.success(request, 'Thanks for volunteering!')

    return render(request, 'tasks/detail.html', context)


def complete(request, task_id):
    job = get_object_or_404(Job, pk=task_id)
    context = {
        'job': job,
        'backUrl': '..',
        'title': 'How did it go?',
        'heading': 'How did it go?'
    }

    if request.method == "POST":
        messages.success(request, 'Success')
        return redirect('tasks:detail', task_id=task_id)

    return render(request, 'tasks/complete.html', context)
