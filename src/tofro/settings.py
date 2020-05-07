"""
Django settings for tofro project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import copy
from django.utils.log import DEFAULT_LOGGING
import os


# Required environment variables. These are loaded automatically
# by docker-compose, and defined in the .env file.
DJANGO_ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost").split(",")
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "012345")
POSTGRES_DB = os.getenv('POSTGRES_DB', 'perioddignitydb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'friendly')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Pa55word')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres-server')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
DEBUG = os.getenv("DEBUG", "True") == "True"


# Email settings.
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "test")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "test")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True

# Send emails in prod, print to console in development.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else \
                'django.core.mail.backends.smtp.EmailBackend'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY

# List of servers that Django will accept requests from.
ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS

# Specify the User model.
# AUTH_USER_MODEL = 'users.User'

# Application definition
INSTALLED_APPS = [
    'markup-help',
    'assets',
    'users',
    'invites',
    'actions',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize'
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add the debug toolbar.
if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE


def show_toolbar(request):
    if request.is_ajax():
        return False
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: not request.is_ajax()
}

# Used by debug_toolbar.
INTERNAL_IPS = [
    '172.30.0.1'  # This is the Docker container's private IP address...
]

ROOT_URLCONF = 'tofro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            # apptemplates allow extending templates from specific apps
            'loaders': [
                'apptemplates.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tofro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = ['core.backends.EmailBackend']


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# WhiteNoise serves the static files via the Python server.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/actions/'

LOGGING = copy.deepcopy(DEFAULT_LOGGING)

# Add a root logger that'll catch the logs of our own apps
LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'INFO'
}
# Prevent Django's logs to be emitted a second time
# by being propaggated to the root logger
LOGGING['loggers']['django']['propagate'] = False

# Customize the logging configuration for development
if DEBUG:
    # Lower the threshold for the console logger
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['loggers']['']['level'] = 'DEBUG'
