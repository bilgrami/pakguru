"""
Django settings for pakguru_site project.

Based on 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import posixpath

from envs import env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3e909706-f2ab-4bed-a9a4-03271bc144a1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
    # Example host name only; customize to your specific host
    "pakguru.azurewebsites.net",
    "127.0.0.1",
    "localhost",
    "pak.guru",
    "www.pak.guru",
]
# Application references
# https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    'pakguru_app.app.PakGuruWebsiteConfig',
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_extensions',
    'rest_framework',
    'django_admin_shell',
 ]

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pakguru_site.urls'

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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

WSGI_APPLICATION = 'pakguru_site.wsgi.application'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
sql_lite_db_path = os.path.join(BASE_DIR, 'db.sqlite3')
if DEBUG and not env('DATABASE_ENGINE'):
    print("sql lite db is located at:", sql_lite_db_path)

DATABASES = {
    'default': {
        'ENGINE': env('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': env('DATABASE_NAME', sql_lite_db_path),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = env('STATIC_URL', '/static/')

STATICFILES_DIR = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['static']))

NOTEBOOK_ARGUMENTS = [
    # '--notebook-dir', 'notebooks',
    # exposes IP and port
    '--ip=0.0.0.0',
    '--port=8888',
    '--allow-root',
    # disables the browser
    '--no-browser',
 ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ],
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.'
        'PageNumberPagination'
        ),
    'PAGE_SIZE': 20
}

# django-admin-shell settings
ADMIN_SHELL_ENABLE = True
ADMIN_SHELL_ONLY_FOR_SUPERUSER = True
ADMIN_SHELL_ONLY_DEBUG_MODE = True
