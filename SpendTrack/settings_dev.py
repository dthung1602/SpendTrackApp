"""
Django DEVELOPMENT settings for SpendTrack project.

These values can by overriden by the environment:

    SECRET_KEY
    
    DB_ENGINE
    DB_NAME
    DB_USER
    DB_PASSWORD
    DB_HOST
    DB_PORT

Optional environmental variables:

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
SECRET_KEY = os.getenv('SECRET_KEY', '5icu55xf=(jv_3tp@@3i02hg9l7(tofd!8@+2uw0ma!4xmqeex')

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
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'spendtrack'),
        'USER': os.getenv('DB_USER', 'spendtrackuser'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'r8XBGQK1As9KLDlJKV8g'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '')
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

# Login logout

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = '/'

LOGIN_URL = 'account:login'

# Email

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sentemails")

######################################
#             APP CONFIG             #
######################################

APP_VERSION = "DEV"

CONTACT_GITHUB = 'https://github.com/' + os.getenv('CONTACT_GITHUB', 'someone')

CONTACT_EMAIL = 'mailto:' + os.getenv('CONTACT_EMAIL', 'someone@somewhere')

CONTACT_FACEBOOK = 'https://www.facebook.com/' + os.getenv('CONTACT_FACEBOOK', 'somebody')

VIEW_SUMMARIZE_DATE_RANGE_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_YEAR_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_MONTH_DEFAULT_PAGE_SIZE = 10

VIEW_SUMMARIZE_WEEK_DEFAULT_PAGE_SIZE = 10

MODEL_CATEGORY_HIERARCHY_MAX_DEPTH = 3

MODEL_PLAN_COMPARE_EQUAL_EPSILON = 0.1
