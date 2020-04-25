import datetime
from django.shortcuts import render

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
def index(request):
  context = {
    'tasks': filter(mineFilter, tasks)
  }
  return render(request, 'helpers/index.html', context)

def available(request):
  context = {
    'tasks': filter(availableFilter, tasks)
  }
  return render(request, 'helpers/index.html', context)

def completed(request):
  context = {
    'tasks': filter(completedFilter, tasks)
  }
  return render(request, 'helpers/index.html', context)