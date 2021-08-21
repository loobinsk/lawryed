"""
Base settings to build other settings files upon.
"""

from datetime import timedelta
# from celery.schedules import crontab
from os import cpu_count

import environ

ROOT_DIR = (
    environ.Path(__file__) - 3
)  # (lawyerd/config/settings/base.py - 3 = lawyerd/)
APPS_DIR = ROOT_DIR.path("lawyerd")

env = environ.Env()

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path(".env")))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"
LANGUAGES = [('en', 'English'), ]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
USE_I18N = False
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [ROOT_DIR.path("locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'config.django_suit_app.SuitConfig',
    # 'suit',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "django_celery_beat",
    # "bootstrap_datepicker_plus",
    "widget_tweaks",
    "django_countries",

    "reversion",
    "dbtemplates",

]

LOCAL_APPS = [
    "users.apps.UsersConfig",
    "poster.apps.PosterConfig",
    "feedback",
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "lawyerd.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
#LOGIN_REDIRECT_URL = "users:redirect"
LOGIN_REDIRECT_URL = "home"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/staticfiles/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR("media"))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "dbtemplates.loader.Loader",
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# https://django-dbtemplates.readthedocs.io/en/latest/settings/
DBTEMPLATES_USE_CODEMIRROR = True
DBTEMPLATES_ADD_DEFAULT_SITE = True
# DBTEMPLATES_USE_REVERSION = True

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = env(
#     "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
# )
# https://docs.djangoproject.com/en/2.2/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""mmmsvit@gmail.com""", "mmmsvit@gmail.com")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "%(levelname)s %(asctime)s %(module)s "
#                       "%(process)d %(thread)d %(message)s"
#         }
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         }
#     },
#     "root": {"level": "INFO", "handlers": ["console"]},
# }

# Celery
# ------------------------------------------------------------------------------
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
CELERY_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = "lawyerd.users.adapters.AccountAdapter"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = "lawyerd.users.adapters.SocialAccountAdapter"

# Your stuff...
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

INSTALLED_APPS += [
    'cacheops',

    # 'rest_framework',
    'rest_framework.authtoken',  # new!
    'rest_auth',  # new!
    'rest_framework_datatables',
    'rest_framework_swagger',
    'mathfilters',
    'explorer',
    'captcha',
    'tinycontent',
    # 'background_task',

    # 'plans',
    # 'ordered_model',

    # 'related_admin',
    'ordered_model',
    'plans_payments',
    'plans',

    'api.v1',
    'products',
    'complaint',
    # 'poster',
    'project',
    # 'company',
    # 'price',
]

# del CELERY_BEAT_SCHEDULER

# BACKGROUND_SITE_SCANS_THREADS = cpu_count()
# BACKGROUND_SITE_SCANS_THREADS = 1

# domain_check_tasks = {f'domain_check-{key}': {
#     'task': 'lawyerd.products.tasks.domain_check',
#     "schedule": timedelta(seconds=3),
#     # "ignore_result": True,  # TODO, check
#     'args': None
# } for key in range(BACKGROUND_SITE_SCANS_THREADS),
# }

# Other Celery settings
# CELERY_BEAT_SCHEDULE = {
#     # проверка сайтов на живучесть, наличие форм для подписки
#     f'domain_check-{key}': {
#         'task': 'lawyerd.products.tasks.domain_check',
#         "schedule": timedelta(seconds=3),
#         # "ignore_result": True,  # TODO, check
#         'args': None
#     } for key in range(BACKGROUND_SITE_SCANS_THREADS),
# }
#
# CELERY_BEAT_SCHEDULE['update_in_progress_orders'] = {
#     'task': 'lawyerd.orders.tasks.update_in_progress_orders',
#     'schedule': timedelta(seconds=60),
#     'args': None
# }


# CELERY_ROUTES = {
#     'lawyerd.compliant.tasks.complaint_work': {'queue': 'compliant_work'},
#     # 'core.tasks.quick_task': {'queue': 'quick_queue'},
# }

# CELERY_IGNORE_RESULT = True
# CELERY_ALWAYS_EAGER = True
# CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


# CELERY_BEAT_SCHEDULE = {
#     # фикс некотректных задач (умер процес обработки но обозначен как в обработке и т.д...)
#     'handle_new_complaint_fix': {
#         'task': 'lawyerd.poster.tasks.handle_new_complaint',
#         # 'task': 'complaint.models.complaint_work',
#         'schedule': timedelta(seconds=60),
#         'description': 'Run not finished tasks (reboot, crach etc... fix)',
#         'args': None
#     },
#
#     'handle_new_complaint_detail_fix': {
#         'task': 'lawyerd.poster.tasks.handle_new_complaint_detail',
#         # 'task': 'complaint.models.complaint_work',
#         'schedule': timedelta(seconds=60),
#         'description': 'Run not finished tasks (reboot, crach etc... fix)',
#         'args': None
#     },
#
# }

# SESSION_ENGINE = 'redis_sessions.session'
#
# SESSION_REDIS = {
#     'host': 'localhost',
#     'port': 6379,
#     'db': 0,
#     'password': '',
#     'prefix': 'session',
#     'socket_timeout': 1
# }
#
#


# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": env("REDIS_URL"),
        "LOCATION": 'redis://localhost',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            "IGNORE_EXCEPTIONS": True,
        },
    }
}

# Alternatively the redis connection can be defined using a URL:
CACHEOPS_ENABLED = True
# CACHEOPS_REDIS = '%s/%s' % (REDIS_KEY, 9)
# CACHEOPS_REDIS = env("REDIS_URL")

CACHEOPS_DEFAULTS = {
    'timeout': 60 * 60  # 1 hour
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    # 'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': 'all'},

    # Cache all queries to Permission
    # 'all' is an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    'auth.permission': {'ops': 'all', 'timeout': 60 * 60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    # '*.*': {'ops': (), 'timeout': 60*60},

    # And since ops is empty by default you can rewrite last line as:
    # '*.*': {'timeout': 60*60},

    # NOTE: binding signals has its overhead, like preventing fast mass deletes,
    #       you might want to only register whatever you cache and dependencies.

    # Finally you can explicitely forbid even manual caching with:
    # 'some_app.*': None,

    # AUTH_USER_MODEL: {'ops': 'all'},
    # 'rest_framework.authentication.token.*': {'ops': 'all'},
    # '*': {'ops': 'all'},
}

# SQL Explorer
# EXPLORER_CONNECTIONS = {'Default': 'readonly'}
# EXPLORER_DEFAULT_CONNECTION = 'readonly'
EXPLORER_CONNECTIONS = {'Default': 'default'}
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_TASKS_ENABLED = True
EXPLORER_SQL_BLACKLIST = ''

# Payments and plans
PAYMENT_MODEL = 'plans_payments.Payment'
# PLANS_CURRENCY = 'EUR'
PLANS_CURRENCY = 'USD'

# account
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'mmmsvittestmail@gmail.com'
# EMAIL_HOST_PASSWORD = 'fewef34r343g4'
#
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# EMAIL_FROM = EMAIL_HOST_USER
# EMAIL_SUBJECT_PREFIX = '[Project] '
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# Email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'i.makushinsky@lawyerd.net'
# EMAIL_HOST_PASSWORD = 'Taketheworld97'
# EMAIL_PORT = 587
# EMAIL_USE_SSL = False
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = "no-reply@lawyerd.net"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'i.makushinsky@lawyerd.net'
EMAIL_HOST_USER = 'dmca@lawyerd.net'
# EMAIL_HOST_PHONE_NUMBER = '+380660448113'
EMAIL_HOST_PASSWORD = 'Taketheworld97'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Google Recaptcha
# get keys from https://www.google.com/recaptcha/intro/index.html
#RECAPTCHA_PUBLIC_KEY = '6LeKip8UAAAAAMxfj2SF3f58g5vLTEs6fMsfixdv'
RECAPTCHA_PUBLIC_KEY = '6LdtJ8wZAAAAADpqttdLcOkpcvymNS3pUMkc6Q3w'
#RECAPTCHA_PRIVATE_KEY = '6LeKip8UAAAAAC1hbZ6p0mT7ecvbBs_bd5mCtJhX'
RECAPTCHA_PRIVATE_KEY = '6LdtJ8wZAAAAADhnTQI37TEWlOYttheFMM6pXYsU'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Google Search
# API_GOOGLE_SEARCH_KEY = 'AIzaSyAHr0KThwPrCDnRdpoXKSvUv-Aq7fauL8c'
# API_GOOGLE_SEARCH_CX = '017749955569768485732:llzekgcngf1'


API_GOOGLE_SEARCH_KEY = 'AIzaSyAHAUeTW7TyTr8XKLY6jfKnarOdc_h0zY4'
API_GOOGLE_SEARCH_CX = '007182509598495812599:cmrijxenlse'

# API KEYS for internal works
API_KEY_INTERNAL = 'rgh8h45g8h4hg8h58h48h5h45nn4bnn4bn554gh45h89g'



# fake key
#API_KEY_2IP = 'c20'
# real key
API_KEY_2IP = '5f5c2b6494988c20'




# YOUTUBE complaint keys
API_YOUTUBE_LOGIN = 'dmca.lawyerd@gmail.com'
API_YOUTUBE_PASSWORD = '!QA2ws3ed'
API_YOUTUBE_PASSWORD = 'QA2ws3edfk59067959h5hJjfkJJd00ssdfnH'

# API_YOUTUBE_LOGIN = 'dmcatakedown50@gmail.com'
# API_YOUTUBE_PASSWORD = '!QA2ws3ed'


API_ANTICAPCTHA_KEY = '84d0f3dde094cf67705959bf04ba5a1d'

API_NO_REPLY_EMAIL = 'no-reply@lawyerd.net'

INTENAL_BASE_URL = 'http://192.168.137.1:8000'

# Sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://7ded81778b834eae9ecc9144265324de@o174225.ingest.sentry.io/1825637",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# create_event = sentry_sdk.capture_message


create_event = print

# ****************************************
# STATIC_ROOT = str(ROOT_DIR("static"))
# STATIC_URL = "https://lawyerd.net/staticfiles/"
