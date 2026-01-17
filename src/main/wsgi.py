import os
import sys
from pathlib import Path

# ===== ここ超重要 =====
BASE_DIR = Path(__file__).resolve().parent.parent  # /var/task/src
sys.path.insert(0, str(BASE_DIR))
# ======================

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

application = get_wsgi_application()
