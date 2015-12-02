import os
from django.core.exceptions import ImproperlyConfigured

try:
    from settings.secret import SECRET_KEY
except ImportError:
    raise ImproperlyConfigured("Please specify a value for the variable SECRET_KEY in project/secret.py")

try:
    from settings.debug import DEBUG
except ImportError:
    DEBUG = False

BASE_DIR         = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DEBUG   = DEBUG
ALLOWED_HOSTS    = ['localhost']
ROOT_URLCONF     = 'settings.urls'
LOGIN_URL        = '/login/'
WSGI_APPLICATION = 'settings.wsgi.application'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT      = '/var/lib/autodidact/static'
STATIC_URL       = '/static/'
MEDIA_ROOT       = '/var/lib/autodidact/uploads'
MEDIA_URL        = '/media/'
TEMPLATE_DIRS    = [os.path.join(BASE_DIR, 'templates')]
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'UTC'
USE_I18N         = False
USE_L10N         = False
USE_TZ           = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autodidact',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
