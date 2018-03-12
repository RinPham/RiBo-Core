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
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['.smartoffice.com', 'localhost:8001'])

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
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
ELASTIC_HOST = env('ELASTIC_HOST')
ELASTIC_PORT = env('ELASTIC_PORT')
API_HOST = env('API_HOST')
API_PORT = env('API_PORT')
MEDIA_URL = "/media/"
PUBLIC_BASE = env('PUBLIC_BASE')

# Application definition
SHINOBI_API = 'shinobi_api'

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'storages',
    'django_q'
    #'easy_thumbnails',
)

LOCAL_APPS = (
    'shinobi_api',
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
    'shinobi_core.dbrouter.DbRouterMiddleware',
    'shinobi_api.middleware.ApiMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'shinobi_api.authentications.KeyPinBackend',
]

ROOT_URLCONF = 'shinobi_core.urls'

WSGI_APPLICATION = 'shinobi_core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# def db_config(prefix='', TEST={}):
#     return {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': prefix + env('DB_NAME'),
#         'USER': env('DB_USER'),
#         'PASSWORD': env('DB_PASS'),
#         'HOST': env('DB_HOST'),
#         'PORT': env('DB_PORT'),
#         'TEST': TEST
#     #        'OPTIONS':  {
#     #            'ssl': {
#     #                'ca': '<PATH TO CA CERT>',
#     #                'cert': '<PATH TO CLIENT CERT>',
#     #                'key': '<PATH TO CLIENT KEY>'
#     #            }
#     #        }
#     }
#
# DATABASES = {
#     'default': db_config(),
#     'test': db_config('test_', {'MIRROR': 'default'})
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  env('DB_SQL_NAME'),#'db_shinobi',
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

DATABASE_ROUTERS = ('shinobi_core.dbrouter.DatabaseRouter',)
DATABASE_APPS_MAPPING = {'no_sql': 'no_sql'}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': env('MEMCACHED_HOST') + ':' + env('MEMCACHED_PORT'),
    },
    "redis_cache": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://" + REDIS_HOST + ":" + REDIS_PORT + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

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
        'shinobi_api.permissions.IsAuthenticated'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'shinobi_api.authentications.TokenAuthentication'
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
                BASE_DIR + '/../../shinobi_core/src/shinobi_core/locale/manual',
                )

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Authentication Settings
AUTH_USER_MODEL = 'shinobi_api.User'  # 'authtools.User'


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

WMA_WINDOW = env('WMA_WINDOW', default=5)
S3_STORAGE_BN = env('S3_STORAGE_BUCKET', default="vms-dev-storage")
S3_STORAGE_EP = '%s.s3.amazonaws.com' % S3_STORAGE_BN

AWS_SENSOR_BN = env('AWS_SENSOR_BN', default='vms-dev-storage')
AWS_SENSOR_LOC = env("AWS_SENSOR_LOC", default="sensor")

AWS_STATIC_BN = env('AWS_STATIC_BN')
AWS_ID = env('AWS_ID')
AWS_SECRET = env('AWS_SECRET')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STATIC_BN

SUPPORT_EMAIL = env('SUPPORT_EMAIL', default='support@smartoffice.com')

BCC_EMAIL_ADDRESS = env('BCC_EMAIL_ADDRESS', default='support@smartoffice.com')
ALLOWED_EMAILS = env('ALLOWED_EMAILS', default='*')
SUPPORT_PHONE = env('SUPPORT_PHONE', default='xxx-xxx-xxxx')

#mongodb
SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'