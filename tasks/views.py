import datetime
from django.shortcuts import render, redirect
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
    task = next(filter(lambda t: t['id'] == task_id, tasks))
    context = {
        'task': task,
        'backUrl': '.',
        'title': "How you can help",
        'heading': f'Help with {task["type"]}<br>in {task["ward"]}'
    }

    if request.method == "POST":
        messages.success(request, 'Thanks for volunteering!')

    return render(request, 'tasks/detail.html', context)


def complete(request, task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    context = {
        'task': next(task),
        'backUrl': '..',
        'title': 'How did it go?',
        'heading': 'How did it go?'
    }

    if request.method == "POST":
        messages.success(request, 'Success')
        return redirect('tasks:detail', task_id=task_id)

    return render(request, 'tasks/complete.html', context)
