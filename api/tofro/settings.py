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
from os.path import join as join_path

# Required environment variables. These are loaded automatically
# by docker-compose, and defined in the .env file.
DJANGO_ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", "localhost").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS","").split(",")
DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "012345")
POSTGRES_DB = os.getenv('POSTGRES_DB', 'perioddignitydb')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'friendly')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'Pa55word')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'postgres-server')
DATABASE_PORT = os.getenv('DATABASE_PORT', '5432')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
DEBUG = os.getenv("DEBUG", "True") == "True"
RUN_ENV = os.getenv('RUN_ENV', None)

DJANGO_ADMIN_LOCATION = os.getenv("DJANGO_ADMIN_LOCATION", "admin")

# ensure
if not RUN_ENV:
    print('warning: RUN_ENV is not set')
    assert DEBUG is True
    RUN_ENV = 'local-dev'

# Email settings.
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "test")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "test")
NOTIFICATIONS_FROM = os.getenv("NOTIFICATIONS_FROM", "ToFro")
DEFAULT_FROM_EMAIL = f"{NOTIFICATIONS_FROM} <{EMAIL_HOST_USER}>"
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
    'admin_auto_filters',
    'django_admin_listfilter_dropdown',
    'actions',
    'categories',
    'pages_and_menus',
    'core',
    'markup_help',
    'notifications',
    'users',
    "django_rq",
    'sitetree',
    'crispy_forms',
    'django_inlinecss',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'admin_overrides',
    'rest_framework',
    'axes',

]
if DEBUG:
    # ensures whitenoise is used in development, as recommended:
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
    INSTALLED_APPS.insert(-1, 'django_extensions')

    #INSTALLED_APPS.insert(0, 'django_werkzeug')


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'axes.middleware.AxesMiddleware',
]


# Necessary for Flatpage
SITE_ID = 1

# Add the debug toolbar.
if DEBUG:
    pass
    INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: not request.is_ajax()
}

# Used by debug_toolbar.
INTERNAL_IPS = [
    '172.30.0.1',  # This is the Docker container's private IP address...
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
                'core.context_processors.settings',
                'core.context_processors.show_kites'
            ],
        },
    },
]
WSGI_APPLICATION = 'tofro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
#        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRES_DB,
        'USER': POSTGRES_USER,
        'PASSWORD': POSTGRES_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT
    }
}


# Redis queue settings.
RQ_QUEUES = {
    'default': {
        'HOST': 'tofro-redis',
        'PORT': REDIS_PORT,
        'DB': 0,
        'DEFAULT_TIMEOUT': 500
    }
}
# Sessions

SESSION_COOKIE_AGE = 1200
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 86400
    CSRF_COOKIE_SECURE = True


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

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'core.backends.EmailBackend',
]
# N.B. This is set in tofro.views.PasswordResetConfirmView


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Two locale paths to differenciate between our own messages
# which will be in `locale` and the overriding of messages
# from existing apps
# https://stackoverflow.com/a/41945558
LOCALE_PATHS = (
    # This is where .po file from Django's `makemessages` command
    # will end up
    os.path.join(BASE_DIR, 'locale'),
    # This is what stores a custom list of messages to override
    os.path.join(BASE_DIR, 'messages_overrides')
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static-built')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    join_path(BASE_DIR, 'static-src'),
    join_path(BASE_DIR, 'parcel-built')
]

if not DEBUG:
    # WhiteNoise serves the static files via the Python server.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# for now, we're disabling django's static 'finder', so all assets need to be in STATIC_ROOT
WHITENOISE_USE_FINDERS = False
WHITENOISE_AUTOREFRESH = DEBUG

# Default template pack for crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/actions/'

LOGGING = copy.deepcopy(DEFAULT_LOGGING)

# Add a root logger that'll catch the logs of our own apps
LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'INFO'
}

# uncomment to switch on error logging for server
# LOGGING['handlers']['console_debug_false'] = {
#			'level': 'ERROR',
#			'filters': ['require_debug_false'],
#			'class': 'logging.StreamHandler',
#		}
# LOGGING['loggers']['django']['handlers'].append('console_debug_false')

# Prevent Django's logs to be emitted a second time
# by being propaggated to the root logger
LOGGING['loggers']['django']['propagate'] = False

# Customize the logging configuration for development
if DEBUG:
    # Lower the threshold for the console logger
    LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['loggers']['']['level'] = 'DEBUG'
    LOGGING['loggers']['django.server']['level'] = 'WARNING'
    # Uncomment to log the DB queries (lots of noise though)
    # LOGGING['loggers']['django.db.backends'] = {
    #     'level': 'DEBUG',
    #     'handlers': ['console'],
    # }

# Help configure contact email
COORDINATOR_EMAIL = os.getenv('COORDINATOR_EMAIL', 'contact@example.com')

ADMINS = [("Dan", "dantagg@wildmanherring.com")]

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser'],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.ToFroPagination',
    'DEFAULT_SCHEMA_CLASS':'rest_framework.schemas.coreapi.AutoSchema',
    'PAGE_SIZE': 50

}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Require authentication

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_ONLY_USER_FAILURES = True
AXES_VERBOSE = False

CSP_SCRIPT_SRC = [
    "'self'",
    "cdn.jsdelivr.net",
    "code.jquery.com",
    "cdnjs.cloudflare.com",
    "kit.fontawesome.com"
]

CSP_STYLE_SRC = [
    "'self'",
    "cdn.jsdelivr.net",
    #"ka-f.fontawesome.com",
]

CSP_CONNECT_SRC = [
    "'self'",
    "ka-f.fontawesome.com",
]

