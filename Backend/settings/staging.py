from .base import *

ACCOUNT_EMAIL_VERIFICATION = 'optional'
# Email validation by gmail
EMAIL_HOST_USER = 'pairmhai.wsp@gmail.com'
EMAIL_HOST_PASSWORD = 'PWL-XA2-Rfy-r5b'

DEBUG = False

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
