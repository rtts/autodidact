import os
import ConfigParser
from django.core.exceptions import ImproperlyConfigured

try:
    from secret import SECRET_KEY
except ImportError:
    raise ImproperlyConfigured("Please specify a value for the variable SECRET_KEY in project/secret.py")

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
    raise ImproperlyConfigured("Error parsing configuration file /etc/bps/config.ini: " + e.message)

BASE_DIR         = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DEBUG   = DEBUG
ALLOWED_HOSTS    = ['localhost', 'bps.created.today', 'bps-beta.uvt.nl', 'bps.uvt.nl']
ROOT_URLCONF     = 'urls'
LOGIN_URL        = '/login/'
WSGI_APPLICATION = 'wsgi.application'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'bps', 'static')]
STATIC_ROOT      = '/var/lib/bps/static'
STATIC_URL       = '/static/'
MEDIA_ROOT       = '/var/lib/bps/uploads'
MEDIA_URL        = '/media/'
TEMPLATE_DIRS    = [os.path.join(BASE_DIR, 'bps', 'templates')]
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
    'autodidact'
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
