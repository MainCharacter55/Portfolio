# portfolio_app/views.py
"""
Views for the portfolio_app.

Handles rendering of portfolio pages including home, about, projects, hobbies,
anime, games, and contact functionality. Uses a mix of function-based views
for dynamic content and class-based TemplateViews for static pages.
"""
# ----------------------------------------------------------------------------------------------------

from django.shortcuts import render
from django.views.generic import TemplateView

def home_view(request):
    """
    Render the home page with portfolio information.

    Displays personal information, tagline, featured projects, and skills.
    Context data is currently hardcoded but could be made configurable
    through settings or database models in the future.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered home page template with context.
    """
    context = {
        'my_name': 'Your Name',
        'tagline': 'Python/Django Developer & System Engineer',
        'projects': [
            {'name': 'Another Project(coming soon)', 'link': '#'}
        ],
        'skills': ['Python', 'Django', 'SQLite', 'Web Development', 'Data Persistence'],
    }
    return render(request, 'portfolio_app/pages/home.html', context)

class HobbiesView(TemplateView):
    """
    View for displaying hobbies page.

    A simple template view that renders the hobbies template.
    """
    template_name = "portfolio_app/hobbies/hobbies.html"

class AboutmeView(TemplateView):
    """
    View for displaying about me page.

    A simple template view that renders the about me template.
    """
    template_name = "portfolio_app/pages/about_me.html"

class AnimeView(TemplateView):
    """
    View for displaying anime page.

    A simple template view that renders the anime template.
    """
    template_name = "portfolio_app/hobbies/anime.html"

class GamesView(TemplateView):
    """
    View for displaying games page.

    A simple template view that renders the games template.
    """
    template_name = "portfolio_app/hobbies/games.html"

class ProjectsView(TemplateView):
    """
    View for displaying projects page.

    A simple template view that renders the projects template.
    """
    template_name = "portfolio_app/portfolio/projects.html"
