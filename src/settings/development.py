from .base import *

DEBUG=True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    "pytest_django",

    # apps
    "accounts",
    "courses",
]

AUTH_USER_MODEL="accounts.UserProfile"

DATABASES={
    "default":{
        "ENGINE":"django.db.backends.sqlite3",
        "NAME": BASE_DIR/ "db.sqlite3",
    },
}

USE_TZ=False