import os
import sys

# /var/task/src を確実に通す
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
