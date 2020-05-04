from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

# A copy of django.contrib.auth.decorators.login_required that looks for login_not_required attr


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        login_req = getattr(function, "login_required", True)

        if login_req:
            return actual_decorator(function)
        else:
            return function
    else:
        return actual_decorator

# Decorator to mark a view as not requiring login to access


def login_not_required(f):
    f.login_required = False
    return f
