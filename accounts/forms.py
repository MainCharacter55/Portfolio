# accounts/forms.py
# ----------------------------------------------------------------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, ContactMessage

class CustomUserCreationForm(UserCreationForm):
    """
    Custom form for creating a new user.
    """
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta): # Inherit the Meta from UserCreationForm
        model = CustomUser
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control",
                "autocomplete": "off"
            })

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('subject', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control bg-dark text-success border-success',
            'placeholder': 'Define signal header...'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'form-control bg-dark text-success border-success',
            'placeholder': 'Enter data for transmission...'
        })

class CustomLoginForm(AuthenticationForm):
    # We define the field as 'email'
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def clean(self):
        # Manually map our 'email' field to the internal 'username' expected by Django
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.cleaned_data['username'] = email # Map email to username for the backend
        return super().clean()
    