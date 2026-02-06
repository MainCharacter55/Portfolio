# accounts/models.py
# ----------------------------------------------------------------------------------------------------

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        # Ensure both email and username are passed to the model
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Critical for superusers
        
        # Superuser needs a username since it's in your REQUIRED_FIELDS
        return self.create_user(email, username, password, **extra_fields)

    # This allows Django to find the user using the email field during login
    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    
    # Connect the manager to the model
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 

    def __str__(self):
        return self.email
    
class ContactMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    