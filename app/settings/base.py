import os

import environ
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

# GENERAL
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'America/Fortaleza'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'pt-br'
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0o644
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        # Configurar váriaveis de ambiente no ambiente de produção
        # ---------------------------------------------------------------------
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB', default='postgres'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'HOST': env('POSTGRES_HOST', default='0.0.0.0'),
        'PASSWORD': env('POSTGRES_PASSWORD', default=''),
        'PORT': env('POSTGRES_PORT', default=5432),
    }
}

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'gep.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'gep.wsgi.application'

# APPS
# ----------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'admin_honeypot',
    'auditlog',
    'axes',
    'bootstrap3',
    'ckeditor',
    'ckeditor_uploader',
    'crispy_forms',
    'easy_thumbnails',
    'guardian',
    'maintenance_mode',
    'multiselectfield',
    'notifications',
    'session_security',
    'watson',
    'ajax_datatable',
]

LOCAL_APPS = [
    'account',
    'adm',
    'core',
    'notifier',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = (
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
    'guardian.backends.ObjectPermissionBackend',
)
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = reverse_lazy('account:painel')
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = reverse_lazy('account:login')
LOGOUT_URL = reverse_lazy('account:logout')
# https://docs.djangoproject.com/en/dev/ref/settings/#session-expire-at-browser-close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# PASSWORDS
# ----------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# MIDDLEWARES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'watson.middleware.SearchContextMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'axes.middleware.AxesMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'core.custom_middlewares.ForceChangePasswordMiddleware',
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = (os.path.join('core/static'),)
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# CKEDITOR UPLOAD
# ------------------------------------------------------------------------------
# https://django-ckeditor.readthedocs.io/en/latest/index.html#required-for-using-widget-with-file-upload
CKEDITOR_UPLOAD_PATH = 'uploads/'

# CKEDITOR CONFIGS
# ------------------------------------------------------------------------------
# https://django-ckeditor.readthedocs.io/en/latest/index.html?highlight=config#example-ckeditor-configuration
CKEDITOR_CONFIGS = {
    'default': {
        # 'skin': 'moono',
        'width': 'auto',
        'uiColor': '#dfe4ea',
        'toolbar_YourCustomToolbarConfig': [
            {
                'name': 'clipboard',
                'items': ['-', 'Undo', 'Redo']
            },
            {
                'name': 'editing',
                'items': ['Find', 'Replace', '-', 'SelectAll']
            },

            {
                'name': 'basicstyles',
                'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat']
            },
            {
                'name': 'paragraph',
                'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                          'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl']
            },
            {
                'name': 'links',
                'items': ['Link', 'Unlink', 'Anchor']
            },
            {
                'name': 'insert',
                'items': ['Image', 'Table', 'HorizontalRule', 'SpecialChar', 'PageBreak']
            },

            {
                'name': 'colors',
                'items': ['TextColor', 'BGColor']
            },
            {
                'name': 'tools',
                'items': ['Maximize', 'ShowBlocks']
            },
            '/',
            {
                'name': 'styles',
                'items': ['Styles', 'Format', 'Font', 'FontSize']
            },
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'toolbarCanCollapse': True,
    },
}
# https://django-ckeditor.readthedocs.io/en/latest/index.html?highlight=config#optional-for-file-upload
CKEDITOR_RESTRICT_BY_USER = True
# https://django-ckeditor.readthedocs.io/en/latest/index.html?highlight=config#restricting-file-upload
CKEDITOR_ALLOW_NONIMAGE_FILES = False

THUMBNAIL_ALIASES = {
    '': {
        'thumb': {'size': (240, 140), 'crop': True},
    },
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.count_notifications',
                'maintenance_mode.context_processors.maintenance_mode',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packsms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = env.bool("SESSION_COOKIE_HTTPONLY", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = env.bool("CSRF_COOKIE_HTTPONLY", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = env.bool("SECURE_BROWSER_XSS_FILTER", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'adm/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ('DINTE-TI/SSP-PI', 'dint.ti@ssp.pi.gov.br'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# django-axes
# ------------------------------------------------------------------------------
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-project-settings
AXES_CACHE = 'axes_cache'
AXES_LOCK_OUT_AT_FAILURE = False
# https://django-axes.readthedocs.io/en/latest/4_configuration.html#configuring-reverse-proxies
AXES_PROXY_COUNT = 1
# https://django-axes.readthedocs.io/en/latest/2_installation.html#disabling-axes-system-checks
SILENCED_SYSTEM_CHECKS = ['axes.W003']

# Celery
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ["cookie.taskapp.celery.CeleryAppConfig"]
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60

# Channels config
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             'hosts': [('localhost', 6379)]
#         },
#     },
# }

# django-maintenance-mode
# ------------------------------------------------------------------------------
# https://github.com/fabiocaccamo/django-maintenance-mode#configuration-optional
MAINTENANCE_MODE_IGNORE_SUPERUSER = True
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_STATUS_CODE = 200
