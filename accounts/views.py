# accounts/views.py
# ----------------------------------------------------------------------------------------------------

# accounts/views.py (Top section cleanup)
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from .models import ContactMessage, CustomUser
from .forms import CustomUserCreationForm, ContactForm

User = get_user_model()

# Create your views here.
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        # 1. Rate limit check (1 hour)
        one_hour_ago = timezone.now() - timedelta(hours=1)
        if ContactMessage.objects.filter(user=request.user, created_at__gt=one_hour_ago).count() >= 5:
            messages.error(request, "SYSTEM_ERROR: Rate limit exceeded. Uplink throttled.")
            return redirect('portfolio_app:contact')

        if form.is_valid():
            # 2. Save to Database
            msg_obj = form.save(commit=False)
            msg_obj.user = request.user
            msg_obj.email = request.user.email 
            msg_obj.save()

            # 3. Send Terminal-Formatted Email
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
            x = 2/0

            messages.success(request, "SIGNAL_DISPATCHED: Transmission successful.")
            return redirect('portfolio_app:contact')
    else:
        form = ContactForm()
    
    return render(request, 'portfolio_app/contact.html', {'form': form})

# --- TOKEN GENERATOR LOGIC (Moved to top) ---
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Tied to user ID, timestamp, and active status for security
        return (str(user.pk) + str(timestamp) + str(user.is_active))

account_activation_token = AccountActivationTokenGenerator()

# accounts/views.py

class SignUpView(CreateView):
    model = CustomUser  # Add this line!
    form_class = CustomUserCreationForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('accounts:signup_success')
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        # Clean up unactivated accounts with the same email
        CustomUser.objects.filter(email=email, is_active=False).delete() 
    
        # Save to DB immediately so user.pk exists
        user = form.save() 
        user.is_active = False # Keep locked
        user.save()
        
        # Now generate the activation link data
        current_site = get_current_site(self.request)
        mail_subject = '[SYSTEM_ACTIVATION] Verify your Uplink'
        message = render_to_string('accounts/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        
        to_email = form.cleaned_data.get('email')
        email_obj = EmailMessage(mail_subject, message, to=[to_email])
        email_obj.send()
        
        # We manually handled the redirect by calling super().form_valid(form) 
        # but since we already saved, we should return the final redirect
        return redirect(self.success_url)

class SignUpSuccessView(TemplateView):
    template_name = "accounts/signup_success.html"

class ActivateView(TemplateView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        # Check the token ONCE
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "UPLINK_ESTABLISHED: Your account is now active.")
            return redirect('accounts:login')
        else:
            if user and user.is_active:
                messages.info(request, "NODE_ALREADY_ACTIVE: Please log in.")
                return redirect('accounts:login')
            return render(request, 'accounts/activation_invalid.html')
        
class ResendActivationView(TemplateView):
    template_name = "accounts/resend_activation.html"

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                # --- Re-run the Activation Protocol ---
                current_site = get_current_site(request)
                mail_subject = '[SYSTEM_RE-ACTIVATION] New Uplink Generated'
                message = render_to_string('accounts/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                email_obj = EmailMessage(mail_subject, message, to=[email])
                email_obj.send()
                messages.success(request, "NEW_SIGNAL_SENT: Check your inbox.")
            else:
                messages.info(request, "NODE_ALREADY_ACTIVE: Please log in.")
        except User.DoesNotExist:
            # We use a generic message so hackers don't know which emails exist
            messages.success(request, "If an account exists, a new link has been sent.")
        
        return redirect('accounts:login')

class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/mypage.html"
    
class DeleteAccountView(LoginRequiredMixin, DeleteView):
    template_name = 'accounts/delete_confirm.html'
    success_url = reverse_lazy('portfolio_app:home')

    def get_object(self):
        return self.request.user
    