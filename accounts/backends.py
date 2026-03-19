# accounts/backends.py
"""
Custom authentication backend for email-based login with future username fallback.

This backend is designed to work with the CustomUser model and is compatible
with django-axes for brute-force protection.
"""
# ----------------------------------------------------------------------------------------------------

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from typing import Optional

# Grab the configured user model (CustomUser)
UserModel = get_user_model()

class CustomModelBackend(ModelBackend):
    """
    Authentication backend that supports email or username lookup.

    Although the project currently uses email for login, this backend
    is prepared to fall back to the username field as well. It is
    placed after AxesBackend in `AUTHENTICATION_BACKENDS` so that
    brute-force protection still wraps it.
    """
    def authenticate(
        self,
        request,
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs
    ) -> Optional["UserModel"]:
        """
        Authenticate a user by email or username.

        Args:
            request: The HTTP request object (required by AxesBackend).
            username: Email or username to authenticate (case-insensitive).
            password: The user's plaintext password.
            **kwargs: Additional keyword arguments (ignored).

        Returns:
            The authenticated CustomUser if credentials match, None otherwise.
        """
        # Axes requires a request argument; the default ModelBackend also
        # accepts it but doesn't use it. We keep the same signature so that
        # our backend can be wrapped by Axes without breaking.
        if username is None or password is None:
            return None

        # Attempt to fetch the user by either email or username, ignoring case.
        # Using iexact (case-insensitive) allows login with 'User@Example.com'
        # or 'USER@EXAMPLE.COM' matching 'user@example.com' in the database.
        # This is the core logic that would allow 'either' login in the future
        # while still functioning as email-only today.
        try:
            user = UserModel.objects.get(
                Q(email__iexact=username) | Q(username__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
