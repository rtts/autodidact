import os
import sys
import ConfigParser
from django.core.exceptions import ImproperlyConfigured

CONFIG_FILE = '/etc/bps/config.ini'
STATIC_ROOT = '/var/lib/bps/static'
MEDIA_ROOT  = '/var/lib/bps/uploads'

try:
    sys.path.append("/etc/bps")
    from secret import SECRET_KEY
except ImportError:
    raise ImproperlyConfigured("Error retrieving SECRET_KEY")

try:
    from debug import DEBUG
except ImportError:
    DEBUG = False

try:
    configParser = ConfigParser.RawConfigParser()
    configParser.read(CONFIG_FILE)
    db_engine = configParser.get('database', 'engine')
    db_name = configParser.get('database', 'name')
    db_host = configParser.get('database', 'hostname')
    db_user = configParser.get('database', 'username')
    db_pass = configParser.get('database', 'password')
    auth_cas_server = configParser.get('authentication', 'cas_server')
    ALLOWED_HOSTS = [e.strip() for e in configParser.get('authentication', 'allowed_hosts').split(',')]
except ConfigParser.Error as e:
    raise ImproperlyConfigured("Error parsing %s: %s" % (CONFIG_FILE, e.message))

if not DEBUG:
    SESSION_COOKIE_SECURE   = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE      = True
    CSRF_COOKIE_HTTPONLY    = True

PACKAGE_DIR      = os.path.dirname(__file__)
TEMPLATE_DEBUG   = DEBUG
ROOT_URLCONF     = 'bps.urls'
LOGIN_URL        = '/login/'
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION = 'bps.wsgi.application'
TEMPLATE_DIRS    = [os.path.join(PACKAGE_DIR, 'templates')]
STATICFILES_DIRS = [os.path.join(PACKAGE_DIR, 'static')]
STATIC_URL       = '/static/'
MEDIA_URL        = '/media/'
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
    'adminsortable',
    'django_cleanup',
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

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

if auth_cas_server:
    CAS_SERVER_URL = auth_cas_server
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'cas.backends.CASBackend',
    )
    MIDDLEWARE_CLASSES += ('cas.middleware.CASMiddleware',)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    try:
        import livereload.middleware
        MIDDLEWARE_CLASSES += ('livereload.middleware.LiveReloadScript',)
    except ImportError:
        pass

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'syslog': {
         'level': 'INFO',
         'class': 'logging.handlers.SysLogHandler',
         'facility': 'local7',
         'address': '/dev/log',
       },
    },
    'loggers': {
        'django':{
            'handlers': ['syslog'],
            'level': 'INFO',
            'disabled': False
        },
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + db_engine,
        'NAME': db_name,
        'HOST': db_host,
        'USER': db_user,
        'PASSWORD': db_pass,
    }
}
