"""
Django settings for projhub project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w#s5&3+zf4hi#w5fz0ng0!k!$ipw6#lknr31biijv2k3e+68^d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ f'192.168.1.{i}' for i in range(1, 256) ] + [
    'localhost',
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_spectacular',
    'corsheaders',
    'django_python3_ldap',
    'rest_framework',
    'rest_framework.authtoken',
    'user',
    'fabricator',
    'project',
    'task',
    'team',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'projhub.urls'

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

WSGI_APPLICATION = 'projhub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/uploads/'
MEDIA_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/uploads')
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    "COMPONENT_SPLIT_REQUEST": True,
}

AUTHENTICATION_BACKENDS = [
    "django_python3_ldap.auth.LDAPBackend",
]



# The URL of the LDAP server(s).  List multiple servers for high availability ServerPool connection.
LDAP_AUTH_URL = ["ldap://192.168.1.207:3268"]

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# Specify which TLS version to use (Python 3.10 requires TLSv1 or higher)
import ssl
LDAP_AUTH_TLS_VERSION = ssl.PROTOCOL_TLSv1_2

# Specify which TLS ciphers to use.
LDAP_AUTH_TLS_CIPHERS = "ALL"

# Unspecified TLS keyword arguments applied to the connection on the underlying `ldap3` library.
LDAP_AUTH_TLS_ARGS = {}

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = "DC=WBTPL,DC=COM"
# LDAP_AUTH_SEARCH_BASE = ""

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "name": "givenName",
    "email": "mail",
}

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

# Path to a callable that takes a user model, a dict of {ldap_field_name: [value]}
# a LDAP connection object (to allow further lookups), and saves any additional
# user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = None

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users`, `ldap_clean_users` commands will perform an anonymous query.
# LDAP_AUTH_CONNECTION_USERNAME = 'wbtpl@tasksrv'
# LDAP_AUTH_CONNECTION_PASSWORD = 'K@02md8769$!'
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None

# Use SSL on the connection.
LDAP_AUTH_CONNECT_USE_SSL = False

# Set connection/receive timeouts (in seconds) on the underlying `ldap3` library.
LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None

# Unspecified keyword arguments to apply to the connection in the underlying `ldap3` library.
LDAP_AUTH_CONNECT_ARGS = {}

# Set connection pool `active` parameter on the underlying `ldap3` library.
LDAP_AUTH_POOL_ACTIVE = True