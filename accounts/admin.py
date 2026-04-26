# accounts/admin.py
"""
Django admin configuration for the accounts app.

Customizes the admin interface for user management and contact messages,
providing better visibility and filtering for site administrators.
"""
# ----------------------------------------------------------------------------------------------------

from django.contrib import admin
from .models import CustomUser, ContactMessage

class CustomUserAdmin(admin.ModelAdmin):
    """
    Admin interface for CustomUser model.

    Displays user accounts with email (login identifier), username (public profile handle),
    and status flags (is_active, is_staff, is_superuser) for quick identification.
    """
    list_display = ('email', 'username', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)

    fieldsets = (
        ('Account Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important Dates', {
            'fields': ('date_joined', 'last_login'),
            'classes': ('collapse',)  # Collapse by default, expand if needed
        }),
    )

class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ContactMessage model.

    Allows admins to review user contact submissions, sorted newest first.
    Includes filtering by user and date for easy organization.
    """
    list_display = ('subject', 'user', 'email', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('subject', 'message', 'email')
    readonly_fields = ('user', 'email', 'created_at', 'message')  # Prevent accidental edits
    ordering = ('-created_at',)  # Newest messages first

    def has_add_permission(self, request):
        """Prevent admins from manually creating contact messages."""
        return False

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
