from datetime import timedelta
from os.path import join
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('.env')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-*xem9d3&b!_6d6&s-xiaxgw1=#xpj6sul5xecs8^*msb(sohpp'

DEBUG = True

ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'rest_framework',
    "rest_framework_simplejwt",
    "drf_spectacular_sidecar",
    "widget_tweaks",
    "apps",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # ✅ Add this line
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.middleware.SubscriptionCheckMiddleware',
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stickify_db',
        'HOST': 'postgres_service',
        'PORT': '5432',
        "USER": 'postgres',
        "PASSWORD": '1'
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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

# cd  /home/abror/PycharmProjects/Wildberries/ &&  .venv/bin/python3 manage.py deactivate_expired_users
# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = 'static/'
STATIC_ROOT = join(BASE_DIR, 'static')
MEDIA_URL = 'media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=160),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Wildberries',
    'DESCRIPTION': "This project create a sticker for wildberries's products",
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True

}

AUTH_USER_MODEL = "apps.User"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_METHODS = {'email'}
