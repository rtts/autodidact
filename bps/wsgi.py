import os, sys

# For unknown reasons, the "python-path" argument to mod_wsgi's
# WSGIDaemonProcess does NOT set the python path.  To prevent being unable
# to load the settings, we add the parent directory to the path here:

parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_dir)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bps.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
