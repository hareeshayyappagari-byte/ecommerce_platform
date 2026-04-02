"""
Django app configuration for products module.
Registers products application and related configurations.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """Configuration for products app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
