"""
ASGI config for PinBoard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import (
    get_asgi_application,
)

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "PinBoard.settings.dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)

application = get_asgi_application()
