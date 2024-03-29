"""
Django settings for ybs_task project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-22y-!%9j4dj)pxq!%r59j3pwg)!v(e%*3ms=^_w_sn^_n98x(n'

# Don't close connection to the db, sec
CONN_MAX_AGE = 60

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'prices_comparator'
]

MIDDLEWARE = []

ROOT_URLCONF = 'ybs_task.urls'

WSGI_APPLICATION = 'ybs_task.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 5432
    }
}

TIME_ZONE = 'UTC'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
