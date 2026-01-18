from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv  # python-dotenv が必要

# ========================
# .env を読み込む
# ========================
load_dotenv()  # プロジェクトルートの .env を読み込み

# ========================
# BASE_DIR
# src/main/settings.py から src/ を基準にする
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ========================
# Secret & Debug
# ========================
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ========================
# Allowed Hosts
# ========================
# 安全にやる場合
ALLOWED_HOSTS = [
    "django-canape-production.up.railway.app"
]
# ALLOWED_HOSTS = ["*"]

# ========================
# Login URLs
# ========================
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'myapp:person_list'

# ========================
# Installed Apps
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
]

# ========================
# Middleware
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静的ファイル配信用
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

# ========================
# Templates
# ========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# ========================
# Database
# ========================
default_db_url = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")

if default_db_url.startswith("sqlite"):
    DATABASES = {
        "default": dj_database_url.parse(default_db_url)
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            default=default_db_url,
            conn_max_age=600,
            ssl_require=True
        )
    }

# ========================
# Password validation
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# ========================
# Static files
# ========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # 開発用
STATIC_ROOT = BASE_DIR / "staticfiles"    # collectstatic 先
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ========================
# Media files
# ========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================
# Default primary key
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
