from django.contrib.auth.models import User
import os

# Get the admin username and password from the environment.
admin_user = os.getenv("DJANGO_ADMIN", "admin")
admin_password = os.getenv("DJANGO_PASSWORD", "password")

# Create the admin user.
users = User.objects.filter(username=admin_user)
if users:
    admin = users[0]
    admin.set_password(admin_password)
    admin.save()
else:
    admin = User.objects.create_user(
        username=admin_user, is_staff=True, is_superuser=True)
    admin.set_password(admin_password)
    admin.save()
