from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView
#from rest_framework import routers
#from rest_framework.documentation import include_docs_urls
from . import views

# Routers
#router = routers.DefaultRouter()
#router.register(r'api', views.OldActionViewSet)

app_name = 'actions'
urlpatterns = [
    path('<int:action_pk>/', views.pkdetail, name="pkdetail"),
    path('available/', views.ActionsListView.as_view(list_type='available'),
         name="available"),
    path('completed/', views.ActionsListView.as_view(list_type='completed'),
         name="completed"),
    path('coordinator/', views.CoordinatorDashboardView.as_view(), name="coordinator_dashboard"),
    path('coordinator/actions/', views.CoordinatorActionsView.as_view(), name="coordinator_actions"),
    path('coordinator/call/', views.CoordinatorCallView.as_view(), name="coordinate_actions"),
    path('coordinator/call/add/', views.CoordinatorCreateActionReferralView.as_view(), name="add_actions"),
    path('coordinator/action/', views.CoordinatorSingleActionView.as_view(), name="single_action"),
    path('ongoing/', views.ActionsListView.as_view(
        list_type='ongoing'), name="ongoing"),
    path('<action_uuid>/complete/', views.action_feedback, name="complete"),
    path('<action_uuid>/cancel/',
         views.stop_ongoing, name="cancel"),
#    path('api/', include((router.urls, 'app_name'))),
#    path('swagger-ui/', TemplateView.as_view(
#        template_name='api/swagger_ui.html',
#        extra_context={'schema_url':'openapi-schema'}),
#        name='swagger-ui'),
#    path('docs/', include_docs_urls(title='My API service'), name='api-docs'),
    path('<action_uuid>/', views.detail, name="detail"),
    path('', RedirectView.as_view(url='/'), name='index'),
]
