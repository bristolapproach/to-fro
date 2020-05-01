from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'tasks'
urlpatterns = [
    path('<int:task_id>/complete', views.complete, name="complete"),
    path('<int:task_id>', views.detail, name="detail"),
    path('available/', views.JobsListView.as_view(list_type='available'),
         name="available"),
    path('completed/', views.JobsListView.as_view(list_type='completed'),
         name="completed"),
    path('', RedirectView.as_view(url='/'), name='index'),
]
