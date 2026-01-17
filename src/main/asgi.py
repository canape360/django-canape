"""
ASGI config for main project.
"""

import os
from django.core.asgi import get_asgi_application

# Django settings を正しく指定（超重要）
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

# Django ASGI application
django_asgi_app = get_asgi_application()

# lifespan 非対応環境（Vercel）向けにシンプル構成
async def application(scope, receive, send):
    await django_asgi_app(scope, receive, send)
