# accounts/models.py
"""
User authentication and contact message models for the portfolio app.

This module defines:
- CustomUser: A custom Django user model that uses email as the primary
  authentication identifier while maintaining a unique username field for
  future public user search features.
- CustomUserManager: Handles creation of regular and super users with both
  email and username validation.
- ContactMessage: Stores user-submitted contact form messages with rate-limiting
  capability via created_at timestamps.
"""
# ----------------------------------------------------------------------------------------------------

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from typing import Optional

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Manager for CustomUser that handles email-based authentication setup."""

    def create_user(
        self,
        email: str,
        username: str,
        password: Optional[str] = None,
        **extra_fields
    ) -> "CustomUser":
        """
        Create and save a regular user.

        Args:
            email: The user's email address (required, must be unique).
            username: The user's public handle (required, must be unique).
            password: The plaintext password (will be hashed and saved).
            **extra_fields: Additional fields to set on the user (e.g., first_name, last_name).

        Raises:
            ValueError: If email is not provided.

        Returns:
            The newly created and saved CustomUser instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Ensure both email and username are passed to the model
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        username: str,
        password: Optional[str] = None,
        **extra_fields
    ) -> "CustomUser":
        """
        Create and save a superuser (admin) account.

        Automatically sets is_staff, is_superuser, and is_active flags.

        Args:
            email: The superuser's email address (required, must be unique).
            username: The superuser's public handle (required, must be unique).
            password: The plaintext password (will be hashed and saved).
            **extra_fields: Additional fields to set on the user.

        Returns:
            The newly created and saved superuser CustomUser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Critical for superusers
        
        # Superuser needs a username since it's in your REQUIRED_FIELDS
        return self.create_user(email, username, password, **extra_fields)

    def get_by_natural_key(self, email: str) -> "CustomUser":
        """
        Retrieve a user by email (case-insensitive).

        This is called by Django's authentication system to find users
        during login and by the dumpdata/loaddata management commands
        for data serialization.

        Args:
            email: The email address to search for.

        Returns:
            The matching CustomUser instance.

        Raises:
            CustomUser.DoesNotExist: If no user with that email exists.
        """
        return self.get(email__iexact=email)

class CustomUser(AbstractUser):
    # We continue to store both email and username. The email field is used
    # as the authentication identifier (USERNAME_FIELD='email'), but username
    # remains a required, publicly-visible handle.  To support future search
    # features and to prevent duplicates we enforce a uniqueness constraint
    # on the username as well.
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    objects = CustomUserManager() # Connect the custom manager to this model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        """Metadata configuration for CustomUser."""
        ordering = ['-date_joined']  # Show newest users first in admin
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.email
    
class ContactMessage(models.Model):
    """
    Stores user-submitted contact form messages.

    This model is used to store messages from the contact form, allowing
    admins to review user inquiries. The created_at timestamp enables
    rate-limiting logic to prevent spam.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Metadata configuration for ContactMessage."""
        ordering = ['-created_at']  # Show newest messages first in admin
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self) -> str:
        """Return a readable string representation of the contact message."""
        return f"Message from {self.user.email} — {self.subject}"
