from .base import *

ALLOWED_HOSTS = ['*']

LOGGING_SENDER_NAME = 'fastfoldtraffic.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../../db.sqlite3'),
    }
}