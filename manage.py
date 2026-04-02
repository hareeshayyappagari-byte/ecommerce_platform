#!/usr/bin/env python
"""
Django management script for ecommerce_platform application.
This script handles all Django administrative operations.
"""
import os
import sys


def main():
    """
    Main entry point for Django command-line utility.
    Sets DJANGO_SETTINGS_MODULE environment variable and executes commands.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
