from .models import Notification
from django.core import serializers
from django.contrib import admin
from django.contrib.auth.models import User


import logging
logger = logging.getLogger(__name__)


admin.site.register(Notification)
