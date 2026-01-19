from pathlib import Path

# manage.py のあるディレクトリ（= src）を BASE_DIR にする
BASE_DIR = Path(__file__).resolve().parent.parent.parent / "src"

import os

import dj_database_url
from dotenv import load_dotenv

# ========================
# BASE_DIR
# src/main/settings.py から src/ を基準にする
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # => src/

# ========================
# .env を読み込む（起動場所に依存しない）
# ========================
# src/.env を読む。もし django-canape/.env を読むなら BASE_DIR.parent / ".env" に変更。
load_dotenv(BASE_DIR / ".env")


# ========================
# Secret & Debug
# ========================
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")

# "True" だけでなく "1", "true", "yes" も True 扱い（本番事故を防ぐ）
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() in ("1", "true", "yes")

# ========================
# Allowed Hosts
# ========================
if DEBUG:
    ALLOWED_HOSTS = ["*"]
else:
    # 例: ALLOWED_HOSTS=localhost,127.0.0.1,django-canape.onrender.com
    ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h.strip()]

    # 念のための保険（必要なら）
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# ========================
# Login URLs
# ========================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "myapp:person_list"

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
    "myapp",
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
# ========================
# DATABASE_URL があればそれを優先。なければ SQLite（src/db.sqlite3）
default_db_url = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")

# dj_database_url.config だけでほぼOK（sqliteでもpostgresでも対応）
DATABASES = {
    "default": dj_database_url.config(
        default=default_db_url,
        conn_max_age=600,
        # 本番だけ SSL 必須にしたいならここを使う（環境により必須/不要があるため）
        ssl_require=not DEBUG,
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
# Static files
# ========================
STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # ★ Manifest なし版（admin と完全互換）
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
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
# Logging (Renderで500原因をLogsに出す)
# ========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        # 500のときの例外トレースを出す
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        # ついでにDjango全般も見たい場合（多すぎたらWARNINGに）
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

