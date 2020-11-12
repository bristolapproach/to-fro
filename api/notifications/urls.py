from django.urls import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('daily-digest-preview/<int:volunteer_pk>', views.daily_digest_volunteer_email_preview),
    path('weekly-digest-preview/<int:volunteer_pk>', views.weekly_digest_volunteer_email_preview),
]
