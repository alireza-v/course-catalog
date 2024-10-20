from decouple import config

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": config("ENGINE", default=None, cast=str),
        "NAME": config("DB_NAME", default=None, cast=str),
        "USER": config("DB_USER", default=None, cast=str),
        "PASSWORD": config("DB_PASSWORD", default=None, cast=str),
    },
}
