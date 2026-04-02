"""
ASGI configuration for ecommerce_platform application.
ASGI (Asynchronous Server Gateway Interface) supports async operations.
Currently uses default Django ASGI application.
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Get the ASGI application instance
application = get_asgi_application()
