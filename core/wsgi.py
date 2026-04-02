"""
WSGI configuration for ecommerce_platform application.
WSGI (Web Server Gateway Interface) is the Python standard for web servers and applications.
This is used for production deployment with servers like Gunicorn.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Get the WSGI application instance
application = get_wsgi_application()
