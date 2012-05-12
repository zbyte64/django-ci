from django.conf.global_settings import *
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'tests.urls'
SITE_ID = 1

BROKER_BACKEND = 'django'

TEMPLATE_CONTEXT_PROCESSORS += ('ci.context_processors.site',
                                'ci.context_processors.git_rev',)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'djkombu',
    'djcelery',

    'ci',
]

#TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
CELERY_ALWAYS_EAGER = True
