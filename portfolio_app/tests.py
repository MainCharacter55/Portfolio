# portfolio_app/tests.py
"""
Test suite for portfolio_app.

Tests cover view functionality, template rendering, and URL resolution.
"""
# ----------------------------------------------------------------------------------------------------

from django.test import TestCase, Client
from django.urls import reverse

class PortfolioViewsTest(TestCase):
    """
    Test cases for portfolio_app views.

    Tests ensure that all portfolio pages render correctly and return
    appropriate HTTP status codes.
    """

    def setUp(self):
        """Set up test client for view testing."""
        self.client = Client()

    def test_home_view(self):
        """
        Test that the home view renders successfully.

        Verifies that the home page loads with status 200 and contains
        expected context data.
        """
        response = self.client.get(reverse('portfolio_app:home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('my_name', response.context)
        self.assertIn('tagline', response.context)
        self.assertIn('projects', response.context)
        self.assertIn('skills', response.context)

    def test_hobbies_view(self):
        """Test that the hobbies page renders successfully."""
        response = self.client.get(reverse('portfolio_app:hobbies'))
        self.assertEqual(response.status_code, 200)

    def test_aboutme_view(self):
        """Test that the about me page renders successfully."""
        response = self.client.get(reverse('portfolio_app:aboutme'))
        self.assertEqual(response.status_code, 200)

    def test_anime_view(self):
        """Test that the anime page renders successfully."""
        response = self.client.get(reverse('portfolio_app:anime'))
        self.assertEqual(response.status_code, 200)

    def test_games_view(self):
        """Test that the games page renders successfully."""
        response = self.client.get(reverse('portfolio_app:games'))
        self.assertEqual(response.status_code, 200)

    def test_projects_view(self):
        """Test that the projects page renders successfully."""
        response = self.client.get(reverse('portfolio_app:projects'))
        self.assertEqual(response.status_code, 200)
