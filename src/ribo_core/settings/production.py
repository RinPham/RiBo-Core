# In production set the environment variable like this:
#    DJANGO_SETTINGS_MODULE=shinobi_core.settings.production
from .base import *             # NOQA
import logging.config

# For security and performance reasons, DEBUG is turned off
DEBUG = False
TEMPLATE_DEBUG = False

# Must mention ALLOWED_HOSTS in production!

API_BASE = "{0}:{1}".format(API_HOST,API_PORT)
if API_PORT=="80":
    API_BASE = "{0}".format(API_HOST)
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=[API_BASE,'127.0.0.1','.smartoffice.vn','localhost','localhost:8001'])


# Cache the templates in memory for speed-up
loaders = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]),
]

TEMPLATES[0]['OPTIONS'].update({"loaders": loaders})
TEMPLATES[0].update({"APP_DIRS": False})

#Disable rest view
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer',]

# Define STATIC_ROOT for the collectstatic command
STATIC_ROOT = join(BASE_DIR, '..', 'site', 'static')

# Reset logging
# (see http://www.caktusgroup.com/blog/2015/01/27/Django-Logging-Configuration-logging_config-default-settings-logger/)

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'django.log'),
            'formatter': 'verbose'
        },
        'proj_log_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': join(LOGFILE_ROOT, 'shinobi_core.log'),
            'formatter': 'verbose'
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'django.db': {
            'handlers': ['django_log_file'],
            'propagate': True,
            'level': 'ERROR',
        },
        'project': {
            'handlers': ['proj_log_file'],
            'level': 'ERROR',
        },
    }
}

logging.config.dictConfig(LOGGING)

# Media S3 config
MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'shinobi_core.storage.MediaStorage'
#MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
MEDIA_URL = env('MEDIA_URL', default='http://static1.vms.com/media/')

AWS_HEADERS = {
    'Expires': 'Thu, 15 Apr 2050 20:00:00 GMT',
    'Cache-Control': 'max-age=86400000',
}
