"""
Django app configuration for accounts module.
Registers accounts application and related configurations.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuration for accounts app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        """Initialize app - import signals on startup"""
        import accounts.models  # noqa - Triggers signal registration
