import datetime
from django.shortcuts import render, redirect
from django.contrib import messages

from core.models import Job

tasks = [{
    'id': 1,
    'type': 'shopping',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=1),
}, {
    'id': 2,
    'type': 'prescription',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=3)
}, {
    'id': 3,
    'type': 'callback',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=5)
}, {
    'id': 4,
    'type': 'shopping',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=1)
}, {
    'id': 5,
    'type': 'prescription',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=-5)
}, {
    'id': 6,
    'type': 'prescription',
    'ward': 'KW',
    'date': datetime.datetime.now() + datetime.timedelta(days=-8)
}]


def availableFilter(task):
    return task["id"] < 4


def mineFilter(task):
    return task["id"] == 4


def completedFilter(task):
    return task["id"] > 4


# Create your views here.
def index(request):
    jobs = Job.objects.all()
    context = {
        'currentListType': 'mine',
        'title': 'My jobs',
        'heading': 'My jobs',
        'jobs': jobs
    }
    return render(request, 'tasks/index.html', context)


def available(request):
    jobs = Job.objects.all()
    context = {
        'currentListType': 'available',
        'title': 'Available jobs',
        'heading': 'Available jobs',
        'jobs': jobs
    }
    return render(request, 'tasks/index.html', context)


def completed(request):
    jobs = Job.objects.all()
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
