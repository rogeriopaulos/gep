from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY_PRODUCTION', default=':ilJl?h264)xSu3?:P5T#-{9*{g6R0qW><^yWWkg8[Cw`?3Z')  # noqa: E501
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
CELERY_TASK_EAGER_PROPAGATES = env('CELERY_TASK_EAGER_PROPAGATES', default=True)

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
if CELERY_TASK_EAGER_PROPAGATES:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
        'axes_cache': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),  # noqa F405
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # Mimicing memcache behavior.
                # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
                "IGNORE_EXCEPTIONS": True,
            }
        },
        'axes_cache': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = env("EMAIL_PORT", default=1025)

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ['django_extensions', ]   # noqa F405

# django-security-session
# ------------------------------------------------------------------------------
# https://django-session-security.readthedocs.io/en/latest/full.html#module-session_security.settings
SESSION_SECURITY_WARN_AFTER = 43199
SESSION_SECURITY_EXPIRE_AFTER = 43200

# django-axes
# ------------------------------------------------------------------------------
# https://django-axes.readthedocs.io/en/latest/2_installation.html#disabling-axes-components-in-tests
AXES_ENABLED = False
