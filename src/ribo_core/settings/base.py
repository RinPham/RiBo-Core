"""
Django settings for vmscore project.
For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from os.path import dirname
from os.path import join

from . import BASE_DIR
from . import env

DEBUG404 = True
STATICFILES_DIRS = [join(BASE_DIR, '')]
MEDIA_ROOT = join(BASE_DIR, 'media')
GEOIP_PATH = join(BASE_DIR, 'geo')
DOC_URL = '/docs/'
DOC_ROOT = join(BASE_DIR, 'docs')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['*', 'localhost:8001'])

USER_PHOTOS_SYNC_PATH = 'uphotos'
USER_DATA_SYNC_PATH = 'updata'

# Use Django templates using the new Django 1.8 TEMPLATES settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            # insert more TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                # 'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.media',
                # 'django.template.context_processors.tz',
            ],
        },
    },
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')
CSRF_COOKIE_SECURE = True
API_HOST = env('API_HOST')
API_PORT = env('API_PORT')
MEDIA_URL = "/media/"
PUBLIC_BASE = env('PUBLIC_BASE')

# Application definition
RIBO_API = 'ribo_api'

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'storages',
    'django_q'
    #'easy_thumbnails',
)

LOCAL_APPS = (
    'ribo_api',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'template_email',
    # 'django_beanstalkd',
    'rest_framework_mongoengine',
    'django_mongoengine',
)
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ribo_core.dbrouter.DbRouterMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'ribo_core.urls'

WSGI_APPLICATION = 'ribo_core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  env('DB_SQL_NAME'),
        'USER': env('DB_SQL_USER'),
        'PASSWORD': env('DB_SQL_PASS',default=''),
        'HOST': env('DB_SQL_HOST'),   # Or an IP Address that your DB is hosted on
        'PORT': env('DB_SQL_PORT'),
    },
    'no_sql': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

MONGODB_DATABASES = {
    "default": {
        "name": env('DB_NOSQL_NAME'), #'test_database',
        "host": env('DB_NOSQL_HOST'),#'localhost',
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}

DATABASE_ROUTERS = ('ribo_core.dbrouter.DatabaseRouter',)
DATABASE_APPS_MAPPING = {'no_sql': 'no_sql'}

Q_CLUSTER = {
    'name': 'vms',
    'workers': 1,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'django_redis': 'redis_cache'
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        # 'ribo_api.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'ribo_api.authentications.TokenAuthentication'
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'EXPIRED_FOREVER': '2000-10-10 00:00:00'
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='vms_mailer')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='vmsmailer1')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SENDGRID_API_KEY = env('SENDGRID_API_KEY',default='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')

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')

LOCALE_PATHS = (
                # This path is link to public repo
                # Just use while make language file, not use while run app
                BASE_DIR + '/../../RiBo-Core/src/ribo_core/locale/manual',
                )

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Authentication Settings
AUTH_USER_MODEL = 'ribo_api.User'  # 'authtools.User'


BEANSTALK_SERVER = env('BEANSTALK_HOST') + ':' + env('BEANSTALK_PORT')
# beanstalk job name pattern. Namespacing etc goes here. This is the pattern
# your jobs will register as with the server, and that you'll need to use
# when calling them from a non-django-beanstalkd client.
# replacement patterns are:
# %(app)s : django app name the job is filed under
# %(job)s : job name
BEANSTALK_JOB_NAME = '%(app)s.%(job)s'

# Log everything to the logs directory at the top
LOGFILE_ROOT = join(dirname(BASE_DIR), 'logs')

GOOGLE_API_KEY_SERVER = env("GOOGLE_API_KEY_SERVER", default='')

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

SUPPORT_EMAIL = env('SUPPORT_EMAIL', default='support@smartoffice.com')

BCC_EMAIL_ADDRESS = env('BCC_EMAIL_ADDRESS', default='support@smartoffice.com')
ALLOWED_EMAILS = env('ALLOWED_EMAILS', default='*')
SUPPORT_PHONE = env('SUPPORT_PHONE', default='xxx-xxx-xxxx')

#mongodb
SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'