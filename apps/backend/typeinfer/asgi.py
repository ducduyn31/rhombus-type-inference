"""
ASGI config for typeinfer project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "typeinfer.settings")

asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_app,
})