# accounts/templatetags/email_filters.py
"""
Custom Django template filters for email handling.

This module provides filters for safely displaying email addresses
in templates while protecting user privacy.
"""
# ----------------------------------------------------------------------------------------------------

from django import template
from typing import Union

register = template.Library()

@register.filter(name='mask_email')
def mask_email(value: str, visible_chars: int = 3) -> str:
    """
    Masks an email address for privacy display.
    
    Args:
        value (str): The email address to mask
        visible_chars (int): Number of characters to show from username (default: 3)
        
    Returns:
        str: The masked email address, or the original value if invalid
    """
    if not isinstance(value, str) or '@' not in value:
        return value
    
    try:
        # Split email into username and domain parts
        user_part, domain_part = value.split('@', 1) # Split only on first '@'
        
        # Mask the username: show first 3 chars, then asterisks
        if len(user_part) > visible_chars:
            masked_user = user_part[:visible_chars] + "***"
        # For short usernames, append asterisks to reach minimum length
        else:
            masked_user = user_part + "***"
            
        return f"{masked_user}@{domain_part}"
    # Fallback for any unexpected errors(invalid email formats, etc.)
    except Exception:
        return value
    