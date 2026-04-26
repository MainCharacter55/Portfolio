# accounts/urls.py
"""
URL routing for the accounts app.

Defines URL patterns for user authentication (signup, login, logout),
password management (change & reset), account deletion, and email activation.

Password reset follows a 4-step flow:
  1. User requests reset (password_reset)
  2. Confirmation email sent (password_reset_done)
  3. User clicks link and confirms (password_reset_confirm)
  4. Password successfully changed (password_reset_complete)
"""
# ----------------------------------------------------------------------------------------------------

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm, TerminalPasswordChangeForm, TerminalSetPasswordForm

app_name = 'accounts'

urlpatterns = [
    # --- User Registration & Email Activation ---
    path('signup/', views.SignUpView.as_view(), name='signup'),
    
    path('signup_success/', views.SignUpSuccessView.as_view(), name='signup_success'),
    
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name='activate'),
    
    path('resend-activation/', views.ResendActivationView.as_view(), name='resend_activation'),
    
    # --- Login & Logout ---
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/pages/login.html',
            authentication_form=CustomLoginForm
        ),
        name='login'
    ),
    
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/pages/logout.html'), name='logout'),
    
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),

    # --- Password Change (User must be logged in) ---
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/forms/password_change.html',
            form_class=TerminalPasswordChangeForm,
            success_url=reverse_lazy('accounts:password_change_done')
        ),
        name='password_change'
    ),
    
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/pages/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # --- Password Reset (Forgot Password Flow: 4 steps) ---
    # Step 1: User enters email to request password reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name="accounts/pages/password_reset_request.html",
            success_url=reverse_lazy('accounts:password_reset_done'),
            email_template_name='accounts/emails/password_reset_email.html'
        ),
        name='password_reset'
    ),
    
    # Step 2: Confirmation page shown after reset email is sent
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/pages/password_reset_sent.html"
        ),
        name='password_reset_done'
    ),
    
    # Step 3: User clicks email link with uidb64 and token to confirm reset
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/pages/password_reset_confirm.html",
            form_class=TerminalSetPasswordForm,
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    
    # Step 4: Success page shown after password is reset
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/pages/password_reset_complete.html"
        ),
        name='password_reset_complete'
    ),
]
