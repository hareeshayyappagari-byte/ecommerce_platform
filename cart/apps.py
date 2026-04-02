"""
Django app configuration for cart module.
Registers cart application and related configurations.
"""

from django.apps import AppConfig


class CartConfig(AppConfig):
    """Configuration for cart app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
