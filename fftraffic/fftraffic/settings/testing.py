from .base import *

ALLOWED_HOSTS = ['*']


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

LOGGING['loggers']['django']['handlers'] = ['file', 'console']
