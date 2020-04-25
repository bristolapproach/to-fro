from django.urls import path
from . import views

app_name = 'helpers'
urlpatterns = [
    path('<int:task_id>', views.detail, name="detail"),
    path('available/', views.available, name="available"),
    path('completed/', views.completed, name="completed"),
    path('', views.index, name='index'),
]