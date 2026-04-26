# accounts/views.py
"""
Views for user authentication and account management.

Provides user registration with email activation, login/logout, password reset,
password change, account deletion, and a contact form with rate limiting.

Terminal-Styled Theme: Messages use a sci-fi terminal aesthetic for UX consistency.
Email Activation: Uses token-based email links for account verification.
Rate Limiting: Contact form limited to 5 messages per user per hour.
"""
# ----------------------------------------------------------------------------------------------------

# Django core views and mixins
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Django utilities
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import timedelta

# Django messaging and configuration
from django.contrib import messages
from django.conf import settings

# Django email and templates
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

# Django authentication
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model

# Local models and forms
from .models import ContactMessage, CustomUser
from .forms import CustomUserCreationForm, ContactForm

User = get_user_model()

def contact_view(request):
    """
    Handle contact form submissions with rate limiting and email notification.

    Rate limits users to 5 messages per hour to prevent spam.
    Sends email to admin and saves message to database with terminal-styled formatting.

    Args:
        request: HTTP request object.

    Returns:
        Rendered contact.html template with form, or redirect on successful submission.
    """
    if request.method == "POST":
        # Keep guest-facing page design, but block unauthenticated mail submission.
        if not request.user.is_authenticated:
            messages.error(request, "SYSTEM_ERROR: AUTH_GATE required for uplink transmission.")
            return redirect('portfolio_app:contact')

        form = ContactForm(request.POST)
        one_hour_ago = timezone.now() - timedelta(hours=1) # Rate limit check: max 5 messages per user per hour
        recent_count = ContactMessage.objects.filter(
            user=request.user,
            created_at__gt=one_hour_ago
        ).count()

        if recent_count >= 5:
            messages.error(request, "SYSTEM_ERROR: Rate limit exceeded. Uplink throttled.")
            return redirect('portfolio_app:contact')

        if form.is_valid():
            # Save message to database
            msg_obj = form.save(commit=False)
            msg_obj.user = request.user
            msg_obj.email = request.user.email
            msg_obj.save()

            # Send terminal-formatted email to admin
            full_body = (
                f"ORIGIN_USER: {request.user.username}\n"
                f"UPLINK_ADDR: {request.user.email}\n"
                f"SIGNAL_HEADER: {form.cleaned_data['subject']}\n"
                f"---------------------------------\n"
                f"DATA_PAYLOAD:\n{form.cleaned_data['message']}"
            )

            email_obj = EmailMessage(
                subject=f"TERMINAL_SIGNAL: {form.cleaned_data['subject']}",
                body=full_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.EMAIL_HOST_USER],
                reply_to=[request.user.email]
            )
            
            email_obj.send()
            messages.success(request, "SIGNAL_DISPATCHED: Transmission successful.")
            return redirect('portfolio_app:contact')
        
    else:
        form = ContactForm()
    return render(request, 'portfolio_app/pages/contact.html', {'form': form})

# --- Email Verification Token Generator ---
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for email account activation.

    Extends Django's PasswordResetTokenGenerator to create secure, single-use
    tokens that expire and become invalid if the user is already activated.

    The hash includes user PK, timestamp, and activation status for security.
    """
    def _make_hash_value(self, user, timestamp):
        """
        Generate hash value for token.

        Tied to user ID, timestamp, and is_active status so token becomes
        invalid if user is already activated.

        Args:
            user: CustomUser instance.
            timestamp: Token generation timestamp.

        Returns:
            String hash value used in token generation.
        """
        return (str(user.pk) + str(timestamp) + str(user.is_active))

account_activation_token = AccountActivationTokenGenerator()

class SignUpView(CreateView):
    """
    Handle user registration and email activation link generation.

    Creates a new inactive user account and sends an email with an activation link.
    Cleans up any previous unactivated accounts with the same email to prevent duplicates.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "accounts/pages/signup.html"
    success_url = reverse_lazy('accounts:signup_success')
    
    def form_valid(self, form):
        """
        Process valid registration form.

        Saves user (inactive), generates activation token, and sends verification email.

        Args:
            form: Validated CustomUserCreationForm instance.

        Returns:
            Redirect to success page (signup_success).
        """
        email = form.cleaned_data.get('email')

        # Clean up any previous unactivated attempts with same email
        CustomUser.objects.filter(email=email, is_active=False).delete()

        # Save user to database with is_active=False
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # Generate activation link with secure token
        current_site = get_current_site(self.request)
        protocol = 'https' if self.request.is_secure() else 'http'
        mail_subject = '[SYSTEM_ACTIVATION] Verify your Uplink'
        message = render_to_string('accounts/emails/activation_email.html', {
            'user': user,
            'protocol': protocol,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        # Send activation email
        to_email = form.cleaned_data.get('email')
        email_obj = EmailMessage(
            mail_subject,
            message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        email_obj.send()
        return redirect(self.success_url)

class SignUpSuccessView(TemplateView):
    """Display confirmation message after successful user registration."""
    template_name = "accounts/pages/signup_success.html"

class ActivateView(TemplateView):
    """
    Verify email activation link and activate user account.

    Validates the activation token and marks the user account as active.
    Shows appropriate message for valid tokens, already-active accounts, or invalid tokens.
    """
    def get(self, request, uidb64, token):
        """
        Process account activation link.

        Args:
            request: HTTP request object.
            uidb64: Base64-encoded user ID from activation email link.
            token: Activation token from email link.

        Returns:
            - Render activation_success.html if activation is successful
            - Render activation_success.html if account was already active
            - Render activation_success.html with invalid status if token is invalid
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        # Verify token and activate account
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return render(
                request,
                'accounts/pages/activation_success.html',
                {'activation_status': 'activated'}
            )
        else:
            # User already activated
            if user and user.is_active:
                return render(
                    request,
                    'accounts/pages/activation_success.html',
                    {'activation_status': 'already_active'}
                )
            # Invalid token or user not found
            return render(
                request,
                'accounts/pages/activation_success.html',
                {'activation_status': 'invalid'}
            )

class ResendActivationView(TemplateView):
    """
    Resend email activation link for inactive accounts.

    Allows users who lost or didn't receive their initial activation email
    to request a new activation link. Uses generic response message to
    prevent email enumeration attacks.
    """
    template_name = "accounts/pages/resend_activation.html"

    def post(self, request):
        """
        Process resend activation email request.

        Args:
            request: HTTP request containing 'email' POST parameter.

        Returns:
            Redirect to login page.
        """
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                # Generate and send new activation link
                current_site = get_current_site(request)
                protocol = 'https' if request.is_secure() else 'http'
                mail_subject = '[SYSTEM_RE-ACTIVATION] New Uplink Generated'
                message = render_to_string('accounts/emails/activation_email.html', {
                    'user': user,
                    'protocol': protocol,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email_obj = EmailMessage(
                    mail_subject,
                    message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email]
                )
                email_obj.send()
                messages.success(request, "NEW_SIGNAL_SENT: Check your inbox.")
            else:
                messages.info(request, "NODE_ALREADY_ACTIVE: Please log in.")
        except User.DoesNotExist:
            # Use generic message to prevent email enumeration attacks
            messages.success(request, "SIGNAL_STATUS: If this node exists, a new uplink has been dispatched.")
        return redirect('accounts:login')

class MyPageView(LoginRequiredMixin, TemplateView):
    """
    Display user profile and account information page.

    Requires user to be logged in. Shows user details and account-related options.
    """
    template_name = "accounts/pages/profile.html"

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    """
    Handle user account deletion.

    Requires user to be logged in. After confirmation, permanently deletes
    the user account and redirects to home page.
    """
    template_name = 'accounts/pages/delete_confirm.html'
    success_url = reverse_lazy('portfolio_app:home')

    def get_object(self):
        """
        Get the object to delete (the current logged-in user).

        Returns:
            The currently authenticated user.
        """
        return self.request.user
