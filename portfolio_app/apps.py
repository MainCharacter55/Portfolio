# portfolio_app/apps.py
"""
Django app configuration for portfolio_app.

This app handles the core portfolio pages including home, about, projects,
hobbies, anime, games, and contact functionality.
"""
# ----------------------------------------------------------------------------------------------------

from django.apps import AppConfig

class PortfolioAppConfig(AppConfig):
    """
    Configuration for the portfolio_app Django application.

    Attributes:
        default_auto_field (str): Default auto field type for model primary keys.
        name (str): The name of the Django app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_app'
