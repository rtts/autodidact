import os
import sys
import ConfigParser
from django.core.exceptions import ImproperlyConfigured

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
    configParser.read('/etc/bps/config.ini')
    db_engine = configParser.get('database', 'engine')
    db_name = configParser.get('database', 'name')
    db_host = configParser.get('database', 'hostname')
    db_user = configParser.get('database', 'username')
    db_pass = configParser.get('database', 'password')
except ConfigParser.Error as e:
    raise ImproperlyConfigured("Error parsing /etc/bps/config.ini: " + e.message)

PACKAGE_DIR      = os.path.dirname(__file__)
TEMPLATE_DEBUG   = DEBUG
ALLOWED_HOSTS    = ['localhost', 'bps.created.today', 'dev.bps.uvt.nl', 'beta.bps.uvt.nl', 'bps.uvt.nl']
ROOT_URLCONF     = 'bps.urls'
LOGIN_URL        = '/login/'
WSGI_APPLICATION = 'bps.wsgi.application'
TEMPLATE_DIRS    = [os.path.join(PACKAGE_DIR, 'templates')]
STATICFILES_DIRS = [os.path.join(PACKAGE_DIR, 'static')]
STATIC_ROOT      = '/var/lib/bps/static'
STATIC_URL       = '/static/'
MEDIA_ROOT       = '/var/lib/bps/uploads'
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

if DEBUG:
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
