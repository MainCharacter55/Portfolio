# accounts/backends.py
"""
Custom authentication backend for email-based login.

This backend is designed to work with the CustomUser model and is compatible
with django-axes for brute-force protection.
"""
# ----------------------------------------------------------------------------------------------------

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from typing import Optional

# Grab the configured user model (CustomUser)
UserModel = get_user_model()

class CustomModelBackend(ModelBackend):
    """
    Authentication backend that supports email lookup.

    This backend is placed after AxesBackend in `AUTHENTICATION_BACKENDS` so that
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
        Authenticate a user by email.

        Args:
            request: The HTTP request object (required by AxesBackend).
            username: Email to authenticate (case-insensitive).
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

        # Email-only lookup to avoid ambiguous matches and enforce policy.
        try:
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            return None

        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
