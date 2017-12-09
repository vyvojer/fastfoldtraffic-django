from .base import *

ALLOWED_HOSTS = ['*']

LOGGING['loggers']['django']['handlers'] = ['file', 'console']