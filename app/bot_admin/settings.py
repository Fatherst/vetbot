import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from dotenv import load_dotenv
from celery.schedules import crontab


load_dotenv()

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "admin_auth.apps.AdminDialogConfig",
    "client_auth.apps.ClientBotConfig",
    "endpoints.apps.EndpointsConfig",
    "bonuses.apps.BonusesConfig",
    "nps.apps.NpsConfig",
    "appointment.apps.AppointmentConfig",
    "django_celery_beat",
    "django_celery_results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "divan"),
        "USER": os.environ.get("POSTGRES_USER", "divan"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "divan"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "test")
DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

ROOT_URLCONF = "bot_admin.urls"
WSGI_APPLICATION = "bot_admin.wsgi.application"

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
FEEDBACK_RECIPIENT_EMAIL = os.getenv("FEEDBACK_RECIPIENT_EMAIL")

GOOGLE_REVIEW_URL = os.getenv("GOOGLE_REVIEW_URL")
YANDEX_REVIEW_URL = os.getenv("YANDEX_REVIEW_URL")

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_WEBHOOK = os.getenv("BOT_WEBHOOK")

API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

EXPORT_API_KEY = os.getenv("EXPORT_API_KEY")

ENOTE_BASIC_AUTH = os.getenv("ENOTE_BASIC_AUTH")
ENOTE_APIKEY = os.getenv("ENOTE_APIKEY")

CATEGORY_ENOTE_ID = os.getenv("CATEGORY_ENOTE_ID")

ENOTE_BALANCE_DEPARTMENT = os.getenv("ENOTE_BALANCE_DEPARTMENT")
ENOTE_API_URL = os.getenv("ENOTE_API_URL")

CSRF_TRUSTED_ORIGINS = [os.getenv("BOT_WEBHOOK")]

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB_INDEX = os.getenv("REDIS_DB_INDEX")
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_INDEX}"
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_RESULT_BACKEND = "django-db"

USE_EASYSMS = os.getenv("USE_EASYSMS", False) == "True"
EASYSMS_LOGIN = os.getenv("EASYSMS_LOGIN")
EASYSMS_PASSWORD = os.getenv("EASYSMS_PASSWORD")
EASYSMS_ORIGINATOR = os.getenv("EASYSMS_ORIGINATOR")
EASYSMS_URL = os.getenv("EASYSMS_URL")

CLINIC_PHONE = os.getenv("CLINIC_PHONE", "+7 (4922) 49-47-82")
CLINIC_URL = os.getenv("CLINIC_URL", "https://vetfriends.ru")
CLINIC_ON_MAP_URL = os.getenv("CLINIC_ON_MAP_URL", "https://go.2gis.com/h3nrl")
CLINIC_ADDRESS = os.getenv("CLINIC_ADDRESS", "Владимир, Студеная Гора 44а/2")
CLINIC_MANAGER_TG_URL = os.getenv("CLINIC_MANAGER_TG_URL", "https://t.me/vetfriends")

CELERY_BEAT_SCHEDULE = {
    "process_not_accrued_bonuses": {
        "task": "bonuses.tasks.process_not_accrued_bonuses",
        "schedule": crontab(hour="*/4"),
    },
    "process_patients_birthdays": {
        "task": "bonuses.tasks.process_patients_birthdays",
        "schedule": crontab(minute="0", hour="9"),
    },
    "send_appointment_notification": {
        "task": "appointment.tasks.send_appointment_notification",
        "schedule": crontab(hour="11"),
    },
    "send_nps": {
        "task": "nps.tasks.send_nps",
        "schedule": crontab(hour="10"),
    },
}


sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        DjangoIntegration(),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)
