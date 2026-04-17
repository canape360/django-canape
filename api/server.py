from django.core.wsgi import get_wsgi_application
import os

# 環境変数を設定（Vercel 用）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.main.settings")

application = get_wsgi_application()
