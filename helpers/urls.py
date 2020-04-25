from django.urls import path
from . import views

app_name = 'helpers'
urlpatterns = [
    path('available/', views.available, name="available"),
    path('completed/', views.completed, name="completed"),
    path('', views.index, name='index'),
]
