# accounts/forms.py
"""
Custom forms for user authentication, registration, and contact messaging.

This module provides specialized forms that integrate with the CustomUser model,
handle email-based authentication, and manage contact submissions with terminal-styled UI.
"""
# ----------------------------------------------------------------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm
from .models import CustomUser, ContactMessage

# ===== CSS Classes (Reusable Constants) =====
FORM_CONTROL_CLASS = "form-control"
TERMINAL_STYLE_CLASSES = "form-control bg-dark text-success border-success"

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for user registration using email instead of username.
    
    Extends Django's UserCreationForm to:
    - Use email as a required field
    - Apply Bootstrap form-control styling
    - Disable autocomplete for security
    """
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta): # Inherit the Meta from UserCreationForm
        """Register CustomUser model with email and username fields."""
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """Apply Bootstrap styling to all form fields."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": FORM_CONTROL_CLASS,
                "autocomplete": "off" # Prevent browser password managers from interfering
            })

class ContactForm(forms.ModelForm):
    """
    Form for users to submit contact messages, styled with a terminal-like appearance.
    This form is linked to the ContactMessage model and includes custom styling
    for a unique user experience.
    """
    class Meta:
        """Configure ContactMessage model fields for display."""
        model = ContactMessage
        fields = ('subject', 'message')

    def __init__(self, *args, **kwargs):
        """Apply terminal-themed styling and placeholders to form fields."""
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({
            'class': TERMINAL_STYLE_CLASSES,
            'placeholder': 'Define signal header...',
            'maxlength': '200'  # Enforce max subject length
        })
        self.fields['message'].widget.attrs.update({
            'class': TERMINAL_STYLE_CLASSES,
            'placeholder': 'Enter data for transmission...',
            'rows': '6'  # Make textarea taller for better UX
        })
        
    def clean_subject(self):
        """Validate subject length and content."""
        subject = self.cleaned_data.get('subject', '').strip()
        if not subject:
            raise forms.ValidationError("SYSTEM_ERROR: SIGNAL_HEADER missing.")
        if len(subject) < 3:
            raise forms.ValidationError("SYSTEM_ERROR: SIGNAL_HEADER must be at least 3 characters.")
        return subject

    def clean_message(self):
        """Validate message length and content."""
        message = self.cleaned_data.get('message', '').strip()
        if not message:
            raise forms.ValidationError("SYSTEM_ERROR: DATA_PAYLOAD missing.")
        if len(message) < 10:
            raise forms.ValidationError("SYSTEM_ERROR: DATA_PAYLOAD must be at least 10 characters.")
        return message

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form using email instead of username.
    
    This form overrides Django's default AuthenticationForm to:
    - Accept email field instead of username
    - Provide a better UX for email-based authentication
    - Map the email field internally to the 'username' field for compatibility
      with Django's authentication backend (which expects 'username')
    """
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': FORM_CONTROL_CLASS,
            'autocomplete': 'email'
    }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': FORM_CONTROL_CLASS,
            'autocomplete': 'current-password'
        })
    )

    def __init__(self, *args, **kwargs):
        """Remove the default 'username' field since we use 'email' instead."""
        super().__init__(*args, **kwargs)
        del self.fields['username'] # Remove default username field

    def clean(self):
        """
        Map the 'email' field to 'username' for Django's authentication backend.
        
        Django's authentication system expects a 'username' field, but we use 'email'.
        This method copies the email value to the username field so the authentication
        backend can properly authenticate the user.
        
        Returns:
            dict: Cleaned form data with username field set to email value
        """
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        # Map email to username for backend authentication
        if email and password:
            self.cleaned_data['username'] = email
        return super().clean()

class TerminalPasswordChangeForm(PasswordChangeForm):
    """Password change form with shared terminal input styling."""

    def __init__(self, *args, **kwargs):
        """Apply unified CSS classes and autocomplete behavior."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': FORM_CONTROL_CLASS,
                'autocomplete': 'off',
            })


class TerminalSetPasswordForm(SetPasswordForm):
    """Password reset confirmation form with shared terminal input styling."""

    def __init__(self, *args, **kwargs):
        """Apply unified CSS classes and autocomplete behavior."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': FORM_CONTROL_CLASS,
                'autocomplete': 'off',
            })
