from .base import *

DEBUG = True

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS += ["localhost", "0.0.0.0"]

REST_FRAMEWORK.update({"TEST_REQUEST_DEFAULT_FORMAT": "json"})
