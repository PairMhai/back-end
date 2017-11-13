from .base import *

VERSION = "v1.4.0-beta.1"


ACCOUNT_EMAIL_VERIFICATION = 'optional'
# Email validation by gmail
EMAIL_HOST_USER = 'pairmhai.wsp@gmail.com'
EMAIL_HOST_PASSWORD = 'PWL-XA2-Rfy-r5b'
# This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEBUG = True

TEST_OUTPUT_FILE_NAME = 'TEST-OUTPUT-DEVELOP-' + str(round(time.time())) + '.xml'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
