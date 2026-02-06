# accounts/urls.py
# ----------------------------------------------------------------------------------------------------

from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

app_name = 'accounts'

urlpatterns = [
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),
         
    path('signup_success/',
         views.SignUpSuccessView.as_view(),
         name='signup_success'),
    
    path('login/',
     auth_views.LoginView.as_view(
         template_name='accounts/login.html',
         authentication_form=CustomLoginForm
     ),
     name='login'),
    
    
    path('logout/',
         auth_views.LogoutView.as_view(template_name='accounts/logout.html'),
         name='logout'),
    
    path('mypage/',
         views.MyPageView.as_view(),
         name='mypage'),

    # --- Password Change (When User is Logged In) ---
    path('password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change_form.html',
             success_url=reverse_lazy('accounts:password_change_done')
         ), name='password_change'),
         
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ), name='password_change_done'),

    # --- Password Reset (Forgot Password Flow) ---
    # 1. Request Page
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset_request.html",
             success_url=reverse_lazy('accounts:password_reset_done'),
             email_template_name='accounts/password_reset_email.html'
         ), name='password_reset'),
         
    # 2. "Email Sent" Confirmation
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"
         ), name='password_reset_done'),
         
    # 3. The Link User Clicks (The Critical Part)
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_confirm.html",
             success_url=reverse_lazy('accounts:password_reset_complete')
         ), name='password_reset_confirm'),
         
    # 4. "Reset Successful" Page
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_complete.html"
         ), name='password_reset_complete'),
    
    path('delete-account/',
         views.DeleteAccountView.as_view(),
         name='delete_account'),
    
    # ... existing paths ...
    path('activate/<uidb64>/<token>/',
         views.ActivateView.as_view(),
         name='activate'),
    
    path('resend-activation/',
         views.ResendActivationView.as_view(),
         name='resend_activation'),
]
