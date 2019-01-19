"""
Django PRODUCTION settings for SpendTrack project.

The environment must provide the following variable:

    SECRET_KEY

                            DB_ENGINE
                            DB_NAME
                            DB_USER
    DATABASE_URL     or     DB_PASSWORD
                            DB_HOST
                            DB_PORT

    CONTACT_GITHUB
    CONTACT_EMAIL
    CONTACT_FACEBOOK

"""

import os

DEBUG = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

######################################
#          DJANGO CONFIG             #
######################################

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

SECURE_SSL_REDIRECT = True

# Database
# This configurations is the default and will be overridden if environment variable $DATABASE_URL exists
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT')
    }
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

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Login logout

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = 'login'

######################################
#             APP CONFIG             #
######################################

APP_VERSION = "1.2"

CONTACT_GITHUB = 'https://github.com/' + os.environ.get('CONTACT_GITHUB')

CONTACT_EMAIL = 'mailto:' + os.environ.get('CONTACT_EMAIL')

CONTACT_FACEBOOK = 'https://www.facebook.com/' + os.environ.get('CONTACT_FACEBOOK')

VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE = os.getenv('VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE', 10)

VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE = os.getenv('VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE', 10)

VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE = os.getenv('VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE', 10)

VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE = os.getenv('VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE', 10)

MODEL_CATEGORY_HIERARCHY_MAX_DEPTH = os.getenv('MODEL_CATEGORY_HIERARCHY_MAX_DEPTH', 3)

MODEL_PLAN_COMPARE_EQUAL_EPSILON = os.getenv('MODEL_PLAN_COMPARE_EQUAL_EPSILON', 0.1)

######################################
#     HEROKU DEPLOYMENT CONFIG       #
######################################

import django_heroku

django_heroku.settings(locals())
