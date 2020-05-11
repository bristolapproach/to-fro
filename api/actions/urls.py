from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'actions'
urlpatterns = [
    path('<int:action_id>/complete', views.complete, name="complete"),
    path('<int:action_id>', views.detail, name="detail"),
    path('available/', views.ActionsListView.as_view(list_type='available'),
         name="available"),
    path('completed/', views.ActionsListView.as_view(list_type='completed'),
         name="completed"),
    path('', RedirectView.as_view(url='/'), name='index'),
]
