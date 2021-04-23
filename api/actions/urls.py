from django.urls import path, include
from django.views.generic.base import RedirectView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from . import views

# Routers
router = routers.DefaultRouter()
router.register(r'api', views.ActionViewSet)

app_name = 'actions'
urlpatterns = [
    path('<int:action_pk>/', views.pkdetail, name="pkdetail"),
    path('available/', views.ActionsListView.as_view(list_type='available'),
         name="available"),
    path('completed/', views.ActionsListView.as_view(list_type='completed'),
         name="completed"),
    path('ongoing/', views.ActionsListView.as_view(
        list_type='ongoing'), name="ongoing"),
    path('<action_uuid>/complete/', views.action_feedback, name="complete"),
    path('<action_uuid>/cancel/',
         views.stop_ongoing, name="cancel"),
    path('<action_uuid>/', views.detail, name="detail"),
    path('api/', include((router.urls, 'app_name'))),
    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
    path('', RedirectView.as_view(url='/'), name='index'),
]
