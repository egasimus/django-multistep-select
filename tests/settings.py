import os

# Make sure 'multistep_select' is on the path.
try:
    import multistep_select  # noqa
except ImportError:
    import sys
    sys.path.insert(0, os.pardir)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite')}}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
SECRET_KEY = '#qu!l*b=nep60+$my-y=tio9h+@k7y1k)f&l168(q4+=!&vf8d'
TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',)
MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',)
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'tests'
)
