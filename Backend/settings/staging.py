from .base import *

VERSION = "1.0.0-test.1"

ACCOUNT_EMAIL_REQUIRED = 'true'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # | optional
# Email validation by gmail
EMAIL_HOST_USER = 'pairmhai.wsp@gmail.com'
EMAIL_HOST_PASSWORD = 'PWL-XA2-Rfy-r5b'
# This did the trick
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://h:pfe4886f78c30f6c3ba1d719a9f08cee38af02104d24c462dac3aceee5ce8a663@ec2-34-206-245-231.compute-1.amazonaws.com:54089",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
