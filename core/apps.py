"""
Django app configuration for core module.
Registers core application handlers and customizations.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for core Django application.
    This app handles project-wide settings and utilities.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
