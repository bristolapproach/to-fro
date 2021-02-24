from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'actions'
urlpatterns = [
    path('<int:action_id>/cancel/',
         views.stop_ongoing, name="cancel"),
    path('<int:action_id>/complete/', views.action_feedback, name="complete"),
    path('<int:action_pk>/', views.pkdetail, name="pkdetail"),
    path('available/', views.ActionsListView.as_view(list_type='available'),
         name="available"),
    path('completed/', views.ActionsListView.as_view(list_type='completed'),
         name="completed"),
    path('ongoing/', views.ActionsListView.as_view(
        list_type='ongoing'), name="ongoing"),
    path('<action_uuid>/', views.detail, name="detail"),
    path('', RedirectView.as_view(url='/'), name='index'),
]
