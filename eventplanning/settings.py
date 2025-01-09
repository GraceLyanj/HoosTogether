"""
Django settings for eventplanning project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url

# Initialise environment variables
env = os.getenv("ENV", "local")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#+qs$*e@iw2zpjg=l_t5i6fdnk9^72e^^t$^xwu53@32dt2^6q"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "project-a-17-cs3240f24-1ed5c5ff7e3d.herokuapp.com",
    "cs3240-app-564e9287dcdb.herokuapp.com",
]


# Application definition
SITE_ID = 2
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "landing",
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "storages",
]

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True
SOCIALCCOUNT_PROVIDER = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": os.environ.get("CLIENT_ID"),
            "secret": os.environ.get("CLIENT_SECRET"),
            "key": "",
        },
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "eventplanning.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "eventplanning.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Database settings
if env == "ci":
    # CI environment - use an in-memory SQLite database for fast test execution
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "test_db"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
        }
    }

elif env == "production":
    # Production environment - use PostgreSQL, configure via DATABASE_URL
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,  # Keep connections open for 10 minutes
            conn_health_checks=True,  # Enable connection health checks
            ssl_require=True,  # Ensure SSL is required
        )
    }

else:
    # Local development environment - use PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "db"),  # Default name is 'db'
            "USER": os.getenv(
                "POSTGRES_USER", "postgres"
            ),  # Default user is 'postgres'
            "PASSWORD": os.getenv(
                "POSTGRES_PASSWORD", "postgres"
            ),  # Default password is 'postgres'
            "HOST": os.getenv(
                "POSTGRES_HOST", "127.0.0.1"
            ),  # Localhost for development
            "PORT": os.getenv("POSTGRES_PORT", "5432"),  # Default PostgreSQL port
        }
    }
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_REDIRECT_URL = "/login"
LOGOUT_REDIRECT_URL = "/login"

# Configure django-storages for S3
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = "cs3240a17bucket"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_DEFAULT_ACL = None
AWS_S3_REGION_NAME = "us-east-1"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIA_ROOT = "media/"

# Heroku settings
import django_heroku

django_heroku.settings(locals())


# Code from the example linked on the course page:
# SHERRIFF
# Activate Django-Heroku.
# Use this code to avoid the psycopg2 / django-heroku error!
# Do NOT import django-heroku above!
try:
    if "HEROKU" in os.environ:
        import django_heroku

        django_heroku.settings(locals())
except ImportError:
    found = False

SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript from accessing the session cookie
CSRF_COOKIE_HTTPONLY = True  # Prevents JavaScript from accessing the CSRF cookie
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents browsers from MIME-sniffing responses
X_FRAME_OPTIONS = "DENY"