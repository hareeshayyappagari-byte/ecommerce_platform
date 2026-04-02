"""
Django app configuration for orders module.
Registers orders application and related configurations.
"""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Configuration for orders app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
