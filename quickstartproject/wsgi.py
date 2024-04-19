"""
WSGI config for quickstartproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from pprint import pprint

from django.core.wsgi import get_wsgi_application

print("Environment:")
pprint(dict(os.environ))

settings_module = 'quickstartproject.production' if 'APPLICATION_DOMAIN' in os.environ else 'quickstartproject.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
