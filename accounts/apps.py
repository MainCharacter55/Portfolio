# accounts/apps.py
"""
Django app configuration for the accounts application.

This module defines the app configuration including the default auto field
for database models.
"""
# ----------------------------------------------------------------------------------------------------

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    """
    Configuration for the accounts app.

    The accounts app handles user authentication, registration, account management,
    and contact form submissions with email-based verification.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
