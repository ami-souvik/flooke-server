"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2yx5sxd8ih89a=9dx6lnkq(7nq$hhdzht-tmtsz7&#i4l($#a!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
PROJECT_APPS = [
    'basic_auth.apps.AuthConfig',
    'content.apps.ContentConfig',
    'comment.apps.CommentConfig',
    'like.apps.LikeConfig',
    'conversation.apps.ConversationConfig',
    'utils.apps.UtilsConfig'
]
EXTERNAL_APPS = [
    'daphne',
    'channels',
    'corsheaders',
    'rest_framework',
]
DJANGO_ESSENTIALS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = PROJECT_APPS + EXTERNAL_APPS + DJANGO_ESSENTIALS

# Allowed origins
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS').split(',') if os.environ.get('ALLOWED_ORIGINS', None) else []

# https://docs.djangoproject.com/en/dev/ref/settings/#std-setting-MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    'middleware.auth.ApplicationAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls.base'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

ASGI_APPLICATION = 'app.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
# WSGI_APPLICATION = 'app.wsgi.application'

# Envrionment Variables
# Load environment variables from .env file/s
# Initialise environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env.local'))


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'OPTIONS': {
            'application_name': 'flooke-server'
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "basic_auth.User"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    )
}

# Personalized authentication backend
AUTHENTICATION_BACKENDS = ['basic_auth.backends.ModelBackend']

# Simple jwt authentication config
SIMPLE_JWT = {
    # It will work instead of the default serializer(TokenObtainPairSerializer).
    # "TOKEN_OBTAIN_SERIALIZER": "basic_auth.serializers.ObtainTokenSerializer",
    # "TOKEN_REFRESH_SERIALIZER": 'basic_auth.serializers.RefreshTokenSerializer'
}

GRAPHENE = {
    'SCHEMA': 'app.schema.schema'
}