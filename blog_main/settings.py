# settings.py  ── replace your entire file with this ──

from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-30o5_0&ss94@65a^u!l=7$gy-8ur5jzz39n2an^zg_ue0+tz%e')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',          # official SDK only — cloudinary_storage removed
    'blogs',
    'assignments',
    'crispy_forms',
    'crispy_bootstrap4',
    'dashboard',
    'rest_framework',
    'django_filters',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_main.urls'

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
                'blogs.context_processors.get_categories',
                'blogs.context_processors.get_social_links',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_main.wsgi.application'

if os.environ.get("DATABASE_URL"):
    DATABASES = {
        'default': dj_database_url.parse(
            os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'blog_main/static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ──────────────────────────────────────────────
# Cloudinary — official SDK, Django-6-safe
# ──────────────────────────────────────────────
_cld_name   = os.environ.get('CLOUDINARY_CLOUD_NAME')
_cld_key    = os.environ.get('CLOUDINARY_API_KEY')
_cld_secret = os.environ.get('CLOUDINARY_API_SECRET')

if _cld_name:
    cloudinary.config(
        cloud_name=_cld_name,
        api_key=_cld_key,
        api_secret=_cld_secret,
        secure=True,
    )

# ──────────────────────────────────────────────
# Custom Cloudinary storage backend
# (replaces django-cloudinary-storage entirely)
# ──────────────────────────────────────────────
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

@deconstructible
class CloudinaryMediaStorage(Storage):
    """
    Minimal Django Storage backend backed by the official cloudinary SDK.
    Handles ImageField / FileField uploads without django-cloudinary-storage.
    """

    def _open(self, name, mode='rb'):
        # Cloudinary is not a local filesystem; reads go through the URL
        import urllib.request
        url = self.url(name)
        return urllib.request.urlopen(url)

    def _save(self, name, content):
        # Strip extension — Cloudinary stores by public_id
        public_id = os.path.splitext(name)[0]
        result = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
            resource_type='auto',
        )
        # Return the public_id + original extension so Django can rebuild the URL
        ext = os.path.splitext(name)[1]
        return result['public_id'] + ext

    def delete(self, name):
        public_id = os.path.splitext(name)[0]
        cloudinary.uploader.destroy(public_id, resource_type='image')

    def exists(self, name):
        try:
            public_id = os.path.splitext(name)[0]
            cloudinary.api.resource(public_id)
            return True
        except Exception:
            return False

    def url(self, name):
        public_id = os.path.splitext(name)[0]
        ext = os.path.splitext(name)[1].lstrip('.')
        return cloudinary.CloudinaryImage(public_id).build_url(format=ext or 'jpg')

    def size(self, name):
        public_id = os.path.splitext(name)[0]
        info = cloudinary.api.resource(public_id)
        return info.get('bytes', 0)


# ── Storage routing ──
if _cld_name:
    STORAGES = {
        "default": {
            "BACKEND": "blog_main.settings.CloudinaryMediaStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']

# ──────────────────────────────────────────────
# Django REST Framework
# ──────────────────────────────────────────────
from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',
        'user': '60/minute',
        'comments': '5/minute',
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}