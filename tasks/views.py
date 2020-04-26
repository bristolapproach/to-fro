import datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

tasks = [{
  'id': 1,
  'type': 'shopping',
  'ward': 'KW',
  'date': datetime.datetime.now() + datetime.timedelta(days=1),
},{
  'id': 2,
  'type': 'prescription',
  'ward': 'KW',
  'date': datetime.datetime.now() + datetime.timedelta(days=3)
},{
  'id': 3,
  'type': 'callback',
  'ward': 'KW',
  'date': datetime.datetime.now() + datetime.timedelta(days=5)
},{
  'id': 4,
  'type': 'shopping',
  'ward': 'KW',
  'date': datetime.datetime.now() + datetime.timedelta(days=1)
},{
  'id': 5,
  'type': 'prescription',
  'ward': 'KW',
  'date': datetime.datetime.now() + datetime.timedelta(days=-5)
},{
  'id': 6,
  'type': 'prescription',
  'ward': 'KW',
  'date':datetime.datetime.now() + datetime.timedelta(days=-8)
}]

def availableFilter(task):
  return task["id"] < 4

def mineFilter(task):
  return task["id"] == 4

def completedFilter(task):
  return task["id"] > 4


# Create your views here.
@login_required
def index(request):
  context = {
    'currentListType': 'mine',
    'tasks': filter(mineFilter, tasks),
    'title': 'My jobs',
    'heading': 'My jobs',
  }
  return render(request, 'tasks/index.html', context)

def available(request):
  context = {
    'currentListType': 'available',
    'tasks': filter(availableFilter, tasks),
    'title': 'Available jobs',
    'heading': 'Available jobs',
  }
  return render(request, 'tasks/index.html', context)

def completed(request):
  context = {
    'currentListType': 'completed',
    'tasks': filter(completedFilter, tasks),
    'title': 'Completed jobs',
    'heading': 'Completed jobs',
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
    return redirect('tasks:detail', task_id = task_id)

  return render(request, 'tasks/complete.html', context)
