import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))  # ← ★これが命★

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "main.settings"
)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
