from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

# ========================
# .env を読み込む（ローカル向け）
# Render では Environment が優先されるので安全
# ========================
load_dotenv()

# ========================
# BASE_DIR
# src/main/settings.py から src/ を基準にする
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent  # => .../repo/src

# ========================
# Secret & Debug
# ========================
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

# Render/ローカル共通で DEBUG を見れるように統一（DEBUG=True/False）
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# ========================
# Allowed Hosts
# 本番は * を避ける（セキュリティ）
# ========================
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "https://django-canape-gsu2.onrender.com",
    "https://django-canape-1-qmru.onrender.com",
]
# Render でカスタムドメインを使うならここに追加

# ========================
# Login URLs（重複定義を排除）
# ========================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/diary/"
LOGOUT_REDIRECT_URL = "/"

# ========================
# Installed Apps
# ========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # AppConfig を明示指定（ready() を有効化）
    "myapp.apps.MyappConfig",
    "diaryapp",
]

# ========================
# Middleware
# ========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # 静的ファイル配信用
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"

# ========================
# Templates
# ========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

# ========================
# Database
# Render は DATABASE_URL（Postgres）を設定するのが基本
# ローカルで未設定なら sqlite を使う
# ========================
# ========================
# Database
# Render では DATABASE_URL（Supabase）を使用
# ローカルで未設定なら sqlite を使う
# ========================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=True,
    )
}

# ========================
# Password validation
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

# ========================
# Static files (Render / WhiteNoise 対応)
# ========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# src/static を拾う
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ========================
# Media files
# ========================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ========================
# Default primary key
# ========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========================
# Logging（Render logs に 500 の原因を出しやすくする）
# ========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
