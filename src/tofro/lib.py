from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
import logging

logger = logging.getLogger(__name__)

# A copy of django.contrib.auth.decorators.login_required that looks for login_not_required attr


def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        has_permission,
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


def has_permission(user):
    try:
        logging.info('Checking user permissions')
        logging.info('Is authenticated', user.is_authenticated)
        # logging.info('Is a volunteer', user.volunteer)
        return user.is_authenticated and bool(user.volunteer)
    except:
        logging.info('User is not a volunteer')
        # `user.volunteer` might raise a RelatedObjectDoesNotExist
        # if there is no volunteer, in which case, we're not authorized
        return False


def login_not_required(f):
    """
    Decorator to mark the function as not requiring login
    to bypass the verifications done by `login_required`
    """
    f.login_required = False
    return f
