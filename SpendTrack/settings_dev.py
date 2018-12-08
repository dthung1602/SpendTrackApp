"""
Django DEVELOPMENT settings for SpendTrack project.

The environment must provide the following variable:

    SECRET_KEY
    
    DB_ENGINE
    DB_NAME
    DB_USER
    DB_PASSWORD
    DB_HOST
    DB_PORT
    
    CONTACT_GITHUB
    CONTACT_EMAIL
    CONTACT_FACEBOOK
    
"""

import os

DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

######################################
#          DJANGO CONFIG             #
######################################

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'spendtrackapp.apps.SpendtrackappConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'SpendTrack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'SpendTrack.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': os.environ['DB_ENGINE'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT']
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Login

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = 'login'

######################################
#             APP CONFIG             #
######################################

APP_VERSION = "1.1"

CONTACT_GITHUB = 'https://github.com/' + os.environ['CONTACT_GITHUB']

CONTACT_EMAIL = 'mailto:' + os.environ['CONTACT_EMAIL']

CONTACT_FACEBOOK = 'https://www.facebook.com/' + os.environ['CONTACT_FACEBOOK']

VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE = -1

MODEL_CATEGORY_HIERARCHY_MAX_DEPTH = 3

MODEL_PLAN_COMPARE_EQUAL_EPSILON = 0.1
