import os, sys
import logging
from six.moves import configparser
from django.core.exceptions import ImproperlyConfigured
from autodidact.utils import random_string
from .utils import read

if os.path.isfile('/etc/bps/config.ini'):
    CONFIG_FILE = '/etc/bps/config.ini'
elif os.path.isfile('bps/config.ini'):
    CONFIG_FILE = 'bps/config.ini'
else:
    raise ImproperlyConfigured('Could not locate the configuration file {/etc/,}bps/config.ini')

try:
    cfg = configparser.RawConfigParser()
    cfg.read(CONFIG_FILE)
    static_dir    = cfg.get('locations', 'static_dir')
    uploads_dir   = cfg.get('locations', 'uploads_dir')
    secret_key    = cfg.get('locations', 'secret_key')
    db_engine     = cfg.get('database', 'engine')
    db_name       = cfg.get('database', 'name')
    db_host       = cfg.get('database', 'hostname')
    db_user       = cfg.get('database', 'username')
    db_pass       = cfg.get('database', 'password')
    cas_server    = cfg.get('misc', 'cas_server')
    allowed_hosts = cfg.get('misc', 'allowed_hosts')
    https_only    = cfg.get('misc', 'https_only') in ['true', 'True', 'on', 'yes']
    debug         = cfg.get('misc', 'debug') in ['true', 'True', 'on', 'yes']
except configparser.Error as e:
    raise ImproperlyConfigured("Error parsing %s: %s" % (CONFIG_FILE, e.message))

try:
    SECRET_KEY = read(secret_key)
except IOError:
    if debug:
        logging.warning('Secret key not found. Using randomly generated key.')
        SECRET_KEY = random_string(50)
    else:
        raise ImproperlyConfigured('Could not read secret key file specified in config file: "{}"'.format(secret_key))

STATIC_ROOT        = static_dir
MEDIA_ROOT         = uploads_dir
CAS_SERVER_URL     = cas_server
ALLOWED_HOSTS      = [e.strip() for e in allowed_hosts.split(',')]
DEBUG              = debug
ROOT_URLCONF       = 'bps.urls'
LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
WSGI_APPLICATION   = 'bps.wsgi.application'
PACKAGE_DIR        = os.path.dirname(__file__)
TEMPLATE_DIRS      = [os.path.join(PACKAGE_DIR, 'templates')]
STATICFILES_DIRS   = [os.path.join(PACKAGE_DIR, 'static')]
STATIC_URL         = '/static/'
MEDIA_URL          = '/uploads/'
LANGUAGE_CODE      = 'en-us'
TIME_ZONE          = 'UTC'
USE_I18N           = False
USE_L10N           = False
USE_TZ             = True
if https_only and not DEBUG:
    SECURE_SSL_REDIRECT   = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE    = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminsortable',
    'django_cleanup',
    'uvt_user',
    'autodidact',
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

if CAS_SERVER_URL:
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'cas.backends.CASBackend',
    ]
    MIDDLEWARE_CLASSES += ['cas.middleware.CASMiddleware']

if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ('debug_toolbar',)
    except ImportError:
        pass
    try:
        import livereload.middleware
        MIDDLEWARE_CLASSES += ('livereload.middleware.LiveReloadScript',)
    except ImportError:
        pass

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': TEMPLATE_DIRS,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]
SILENCED_SYSTEM_CHECKS = ['1_8.W001']

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

if DEBUG and 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
