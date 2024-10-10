import os
from dotenv import load_dotenv
from .base import *
load_dotenv()

DEBUG=False

DATABASES={
    "default":{
        "ENGINE":"django.db.backends.postgresql",
        "USER":os.getenv("DB_USER"),
        "NAME":os.getenv("DB_NAME"),
        "PASSWORD":os.getenv("DB_PASSWORD"),
    },
}

