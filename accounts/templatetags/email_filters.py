from django import template

register = template.Library()

@register.filter(name='mask_email')
def mask_email(value):
    try:
        email_parts = value.split('@')
        user_part = email_parts[0]
        domain_part = email_parts[1]
        
        # Show first 3 chars, then asterisks, then the domain
        if len(user_part) > 3:
            masked_user = user_part[:3] + "***"
        else:
            masked_user = user_part + "***"
            
        return f"{masked_user}@{domain_part}"
    except (IndexError, AttributeError):
        return value