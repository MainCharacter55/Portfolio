# accounts/tests.py
"""
Unit tests for the accounts app.

This module tests user authentication, registration, and related functionality
to ensure the system works correctly and can be extended safely in the future.
Includes tests for models, authentication backends, and form validation.
Tests use RequestFactory to provide mock HTTP requests needed by AxesBackend.
"""
# ----------------------------------------------------------------------------------------------------

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from .models import CustomUser, ContactMessage
from .forms import CustomUserCreationForm, CustomLoginForm, ContactForm
from .backends import CustomModelBackend
from .views import account_activation_token

User = get_user_model()

class CustomUserModelTest(TestCase):
    """Test the CustomUser model and its manager methods."""
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.assertEqual(user.email, 'admin@example.com')
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.check_password('adminpass123'))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_username_uniqueness(self):
        """Test that usernames must be unique."""
        User.objects.create_user(
            email='user1@example.com',
            username='uniqueuser',
            password='pass123'
        )
        with self.assertRaises(Exception):  # Should raise IntegrityError
            User.objects.create_user(
                email='user2@example.com',
                username='uniqueuser',  # Same username
                password='pass123'
            )

    def test_email_uniqueness(self):
        """Test that emails must be unique."""
        User.objects.create_user(
            email='same@example.com',
            username='user1',
            password='pass123'
        )
        with self.assertRaises(Exception):  # Should raise IntegrityError
            User.objects.create_user(
                email='same@example.com',  # Same email
                username='user2',
                password='pass123'
            )

    def test_get_by_natural_key(self):
        """Test getting user by email (natural key)."""
        user = User.objects.create_user(
            email='natural@example.com',
            username='naturaluser',
            password='pass123'
        )
        retrieved = User.objects.get_by_natural_key('natural@example.com')
        self.assertEqual(user, retrieved)

    def test_str_method(self):
        """Test the string representation of CustomUser."""
        user = User.objects.create_user(
            email='str@example.com',
            username='struser',
            password='pass123'
        )
        self.assertEqual(str(user), 'str@example.com')

class AuthenticationTest(TestCase):
    """
    Test authentication functionality with the CustomModelBackend.
    
    These tests verify that email-based authentication works correctly
    and that the backend properly rejects invalid credentials or inactive users.
    """
    def setUp(self):
        """Create a test user and RequestFactory for authentication tests."""
        self.user = User.objects.create_user(
            email='auth@example.com',
            username='authuser',
            password='authpass123'
        )
        self.backend = CustomModelBackend()
        # RequestFactory provides mock HTTP requests without hitting the network.
        # AxesBackend requires a request object, so we create mock requests here.
        self.factory = RequestFactory()

    def test_authenticate_with_email(self):
        """Test authentication using email."""
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='auth@example.com', password='authpass123')
        self.assertEqual(user, self.user)

    def test_authenticate_with_username(self):
        """Test authentication using username (future-proofing for username-based login)."""
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='authuser', password='authpass123')
        self.assertEqual(user, self.user)

    def test_authenticate_case_insensitive(self):
        """Test that authentication is case-insensitive for email and username."""
        request = self.factory.get('/')
        # Test email case-insensitivity
        user_upper = self.backend.authenticate(request, username='AUTH@EXAMPLE.COM', password='authpass123')
        self.assertEqual(user_upper, self.user)
        # Test username case-insensitivity
        user_mixed = self.backend.authenticate(request, username='AuthUser', password='authpass123')
        self.assertEqual(user_mixed, self.user)

    def test_authenticate_wrong_password(self):
        """Test authentication with wrong password."""
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='auth@example.com', password='wrongpass')
        self.assertIsNone(user)

    def test_authenticate_wrong_email(self):
        """Test authentication with wrong email."""
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='wrong@example.com', password='authpass123')
        self.assertIsNone(user)

    def test_inactive_user_cannot_authenticate(self):
        """Test that inactive users cannot authenticate."""
        self.user.is_active = False
        self.user.save()
        request = self.factory.get('/')
        user = self.backend.authenticate(request, username='auth@example.com', password='authpass123')
        self.assertIsNone(user)

class FormTest(TestCase):
    """
    Test form validation for signup, login, and contact forms.
    
    Ensures all form validation logic works correctly, including email mapping
    in the login form and min-length constraints in the contact form.
    """
    def setUp(self):
        """Prepare a RequestFactory for form tests that need request objects."""
        self.factory = RequestFactory()

    def test_custom_user_creation_form_valid(self):
        """Test CustomUserCreationForm with valid data."""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_email(self):
        """Test CustomUserCreationForm with invalid email."""
        form_data = {
            'username': 'newuser',
            'email': 'invalid-email',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_custom_login_form_valid(self):
        """Test CustomLoginForm with valid data."""
        User.objects.create_user(
            email='login@example.com',
            username='loginuser',
            password='loginpass123'
        )
        form_data = {
            'email': 'login@example.com',
            'password': 'loginpass123'
        }
        # Create a mock request to avoid AxesBackend issues
        request = self.factory.get('/')
        form = CustomLoginForm(data=form_data)
        form.request = request  # Attach request to satisfy AxesBackend
        # Assert form validates and internal mapping eventually happens during clean
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data.get('username'), 'login@example.com')

    def test_custom_login_form_clean_maps_email(self):
        """Test that CustomLoginForm maps email to username internally."""
        User.objects.create_user(
            email='map@example.com',
            username='mapuser',
            password='mappass123'
        )
        form_data = {
            'email': 'map@example.com',
            'password': 'mappass123'
        }
        # Create a mock request to avoid AxesBackend issues
        request = self.factory.get('/')
        form = CustomLoginForm(data=form_data)
        form.request = request  # Attach request to satisfy AxesBackend
        # Validate the form, which populates cleaned_data and invokes clean()
        form.is_valid()
        # Check that email was mapped to username in cleaned_data
        self.assertEqual(form.cleaned_data['username'], 'map@example.com')

    def test_contact_form_valid(self):
        """Test ContactForm with valid data."""
        user = User.objects.create_user(
            email='contact@example.com',
            username='contactuser',
            password='contactpass123'
        )
        form_data = {
            'subject': 'Test Subject',
            'message': 'This is a test message with enough content to pass validation.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_contact_form_subject_too_short(self):
        """Test ContactForm with subject too short."""
        form_data = {
            'subject': 'Hi',  # Too short
            'message': 'This is a test message with enough content to pass validation.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('SYSTEM_ERROR', form.errors['subject'][0])

    def test_contact_form_message_too_short(self):
        """Test ContactForm with message too short."""
        form_data = {
            'subject': 'Test Subject',
            'message': 'Hi'  # Too short
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        self.assertIn('SYSTEM_ERROR', form.errors['message'][0])

class ContactMessageModelTest(TestCase):
    """Test the ContactMessage model."""
    def setUp(self):
        """Create a test user for contact message tests."""
        self.user = User.objects.create_user(
            email='contactmsg@example.com',
            username='contactmsguser',
            password='contactmsgpass123'
        )

    def test_create_contact_message(self):
        """Test creating a contact message."""
        message = ContactMessage.objects.create(
            user=self.user,
            email='contactmsg@example.com',
            subject='Test Subject',
            message='Test message content'
        )
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.subject, 'Test Subject')
        self.assertEqual(message.message, 'Test message content')
        self.assertIsNotNone(message.created_at)


class ActivationFlowTest(TestCase):
    """Test account activation link flow and rendered status page."""

    def setUp(self):
        """Create an inactive account and prepare activation URL params."""
        self.user = User.objects.create_user(
            email='inactive@example.com',
            username='inactiveuser',
            password='inactivepass123',
            is_active=False
        )
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_activation_link_renders_success_page(self):
        """Valid activation token should activate user and show success page."""
        response = self.client.get(
            reverse('accounts:activate', kwargs={'uidb64': self.uidb64, 'token': self.token})
        )

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/pages/activation_success.html')
        self.assertContains(response, 'UPLINK_ESTABLISHED')

    def test_activation_link_for_already_active_user_shows_status_page(self):
        """Already-active users should still get a clear activation status page."""
        self.user.is_active = True
        self.user.save()

        response = self.client.get(
            reverse('accounts:activate', kwargs={'uidb64': self.uidb64, 'token': self.token})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/pages/activation_success.html')
        self.assertContains(response, 'NODE_ALREADY_ACTIVE')

    def test_activation_link_with_invalid_token_shows_invalid_status(self):
        """Invalid tokens should render activation status page with invalid state."""
        response = self.client.get(
            reverse('accounts:activate', kwargs={'uidb64': self.uidb64, 'token': 'invalid-token'})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/pages/activation_success.html')
        self.assertContains(response, 'LINK_INTEGRITY_COMPROMISED')
