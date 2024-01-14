from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

SECRET_KEY = 'django-insecure-hpl8i4xz^f&@%&()+yej29a2=x=ah+k9=+js4rhfn_@4pyn33u'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'mptt',
    'django_ckeditor_5',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'analytical',
    'taggit',
    'user_app.apps.UserAppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'site_blog.urls'

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
                'blog.context_processors.get_social_links',
                'blog.context_processors.get_header_categories',
                'blog.context_processors.get_search_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'site_blog.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Novosibirsk'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройка почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Статистика
YANDEX_METRICA_COUNTER_ID = ''
GOOGLE_ANALYTICS_GTAG_PROPERTY_ID = ''

# Админпанель
JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "sticky_actions": True,
    "actions_sticky_top": True,
}
JAZZMIN_SETTINGS = {
    "site_title": "Гастро Блог",
    "site_brand": "Гастро Блог",
}

# CKEditor 5
customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]

CKEDITOR_5_CUSTOM_CSS = 'django_ckeditor_5/admin_dark_mode_fix.css'
CKEDITOR_5_FILE_STORAGE = "blog.storage.CustomStorage"

CKEDITOR_5_CONFIGS = {
    "default": {
        "language": "ru",
        'toolbar': {
            'items': [
                '|', 'heading',
                '|', 'outdent', 'indent',
                '|', 'bold', 'italic', 'link', 'underline', 'strikethrough', 'code', 'subscript', 'superscript',
                'highlight',
                '|', 'codeBlock', 'insertImage', 'bulletedList', 'numberedList', 'todoList',
                '|', 'blockQuote',
                '|', 'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable', 'sourceEditing',
                '|',
            ],
            'shouldNotGroupWhenFull': True
        },
        "image": {
            "toolbar": [
                '|', "imageTextAlternative",
                "|", "imageStyle:alignLeft", "imageStyle:alignRight", "imageStyle:alignCenter", "imageStyle:side",
                "|", "toggleImageCaption",
                "|"
            ],
            "styles": [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
                "tableProperties",
                "tableCellProperties",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
    },
}


LOGOUT_REDIRECT_URL = 'blog:index'
