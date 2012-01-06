import os
import sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, ".."))

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': { "ENGINE": 'django.db.backends.sqlite3'
               , "NAME": 'testdb.sqlite'
               , }
    , }

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = '/static/'
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = (
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = 'oe-9c2c9&z-$o1#+$tta(!-1hn(jm4*(wt^-39gw*$se2ny$02'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'test_project.urls'

TEMPLATE_DIRS = ()

INSTALLED_APPS = ('compress', 'app', 'django_jenkins', )

JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 'django_jenkins.tasks.run_pyflakes',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.django_tests',)

PROJECT_APPS = ['compress','app',]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

COMPRESS_ROOT = os.path.join(os.path.dirname(__file__), "app/tests/testdata/")
COMPRESS_URL = 'http://localhost/static/'
