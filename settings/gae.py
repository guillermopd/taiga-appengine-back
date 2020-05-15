# -*- coding: utf-8 -*-
from google.oauth2 import service_account
import os

# Copyright (C) 2014-2017 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2017 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2017 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2017 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .common import *

#########################################
## GENERIC
#########################################

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taiga',
        'USER': os.getenv('SQL_USER', default='taiga'),
        'PASSWORD': os.getenv('SQL_PASS', default='taiga'),
        'HOST': 'localhost',
    }
}

if 'GAE_INSTANCE' in os.environ:
    DATABASES['default']['HOST'] = '/cloudsql/' + os.getenv('GOOGLE_CLOUD_PROJECT') + ':' + os.getenv('DB_REGION') + ':' + os.getenv('SQL_NAME')

BACKEND_DOMAIN = os.getenv('GAE_SERVICE') + '-dot-' + os.getenv('GOOGLE_CLOUD_PROJECT') + '.appspot.com'
FRONTEND_DOMAIN = os.getenv('GAE_SERVICE') + 'taiga-front-dot-' + os.getenv('GOOGLE_CLOUD_PROJECT') + '.appspot.com'

SITES = {
    "api": {
        "scheme": "https",
        "domain": BACKEND_DOMAIN,
        "name": "api"
    },
    "front": {
        "scheme": "https",
        "domain": FRONTEND_DOMAIN,
        "name": "front"
    },
}

SITE_ID = "api"

# MEDIA_ROOT = '/home/taiga/media'
# STATIC_ROOT = '/home/taiga/static'
MEDIA_URL = 'https://' + BACKEND_DOMAIN + '/media/'
STATIC_URL = 'https://' + BACKEND_DOMAIN + '/static/'

#########################################
## MAIL SYSTEM SETTINGS
#########################################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('SMTP_HOST')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('SMTP_USER')
EMAIL_HOST_PASSWORD = os.getenv('SMTP_PASS')

#DEFAULT_FROM_EMAIL = 'taiga@plasmadev.com'
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


#########################################
## REGISTRATION
#########################################

PUBLIC_REGISTER_ENABLED = False

#########################################
## CELERY
#########################################
# Set to True to enable celery and work in async mode or False
# to disable it and work in sync mode. You can find the celery
# settings in settings/celery.py and settings/celery-local.py
CELERY_ENABLED = False

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = os.getenv('GS_BACKEND_BUCKET')
# GS_DEFAULT_ACL = 'publicRead'
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    "bucket-access.json"
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "complete": {
            "format": "%(levelname)s:%(asctime)s:%(module)s %(message)s"
        }
    },
    "handlers": {
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler",
            "formatter": "complete",
        }
    },
    "loggers": {
        "django": {
            "handlers":["console"],
            "propagate": True,
            "level": "DEBUG",
        },
        "django.request": {
            "handlers":["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "taiga.export_import": {
            "handlers":["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "taiga": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.server": {
            "handlers":["console"],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}
