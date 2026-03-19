# accounts/context_processors.py
"""Shared template context values for account- and portfolio-level templates."""
# ----------------------------------------------------------------------------------------------------

def social_links(_request):
    """Provide external profile links in one place for all templates.

    Args:
        _request: Django HttpRequest object (unused).

    Returns:
        dict: Mapping of social platform keys to profile URLs.
    """
    return {
        "SOCIAL_LINKS": {
            "discord": "https://discord.com/users/835809414031212584",
            "github": "https://github.com/MainCharacter55",
            "instagram": "https://www.instagram.com/",
            "linkedin": "https://www.linkedin.com/in/mohan-khatri-0141b13a9/",
            "tiktok": "https://www.tiktok.com/",
            "twitch": "https://www.twitch.tv/",
            "x": "https://x.com/",
            "youtube": "https://www.youtube.com/",
        }
    }
