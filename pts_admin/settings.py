from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
import dj_database_url

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', '')

DEBUG = True if os.getenv('Debug') == "True" else False

ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_filters',
    'django_ckeditor_5',
    'rest_framework',
    'drf_yasg',

    'users.apps.UsersConfig',
    'projects.apps.ProjectsConfig',

]

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pts_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pts_admin.wsgi.application'


# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL")
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading", "|",
            "bold", "italic", "underline", "link", "|",
            "bulletedList", "numberedList", "|",
            "blockQuote", "|",
            "undo", "redo",
        ],
    }
}
CKEDITOR_5_UPLOAD_PATH = "uploads/"

def environment_callback(request):
    # текст + цвет бейджа
    return ["Production", "danger"]

UNFOLD = {
    # "SHOW_LANGUAGES": True,
    "STYLES": [
        lambda request: static("admin/custom.css"),
        lambda request: static("admin/ckeditor5.css"),
    ],
    "SITE_TITLE": "PTS Админ панель",
    "SITE_HEADER": "PTS Energy",
    "SITE_SUBHEADER": "Панель управления",

    "SITE_LOGO": {
        "light": lambda request: static("logo/logo_dark.svg"),
        "dark": lambda request: static("logo/logo_light.svg"),
    },
    "SITE_ICON": {
        "light": lambda request: static("logo/logo_dark.svg"),
        "dark": lambda request: static("logo/logo_light.svg"),
    },

    "ENVIRONMENT": "pts_admin.settings.environment_callback",

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Управление"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Дашборд"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Проекты"),
                        "icon": "work",
                        "link": reverse_lazy("admin:projects_companyproject_changelist"),
                    },                    
                    {
                        "title": _("Пользователи"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },            
        ],
    },
}

# Locale
LOCALE_PATHS = [BASE_DIR / "locale"]

# Internationalization
LANGUAGE_CODE = "ru"

LANGUAGES = (
    ("ru", "Русский"),
    ("en", "English"),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Email
EMAIL_CODE_LENGTH = 6
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_USE_SSL = False
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'