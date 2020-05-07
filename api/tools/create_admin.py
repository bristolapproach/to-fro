from users.models import UserRole
import os

# Load our custom User model through Django.
from django.contrib.auth import get_user_model
User = get_user_model()

from users.models import Coordinator


# Get the admin details from the environment.
first_name = os.getenv("DJANGO_ADMIN_FIRSTNAME", "Admin")
last_name = os.getenv("DJANGO_ADMIN_LASTNAME", "")
password = os.getenv("DJANGO_ADMIN_PASSWORD", "password")

# Check if the admin user exists.
admin = Coordinator.objects.filter(username='admin',
    first_name=first_name, last_name=last_name,
    role__contains=UserRole.COORDINATOR).first()
if admin:
    # Update password.
    admin.set_password(password)
    admin.save()
else:
    # Create the admin user.
    admin = Coordinator.objects.create_user(
        username='admin', first_name=first_name, 
        last_name=last_name, role=UserRole.COORDINATOR,
        is_superuser=True)
    admin.set_password(password)
    admin.save()
