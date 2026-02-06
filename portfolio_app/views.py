# portfolio_app/views.py
# ----------------------------------------------------------------------------------------------------

from django.shortcuts import render
from django.conf import settings
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import EmailMessage

# Create your views here.
def home_view(request):
    context = {
        'my_name': 'Your Name',
        'tagline': 'Python/Django Developer & System Engineer',
        'projects': [
            {'name': 'Another Project(coming soon)', 'link': '#'}
        ],
        'skills': ['Python', 'Django', 'SQLite', 'Web Development', 'Data Persistence'],
    }
    return render(request, 'portfolio_app/home.html', context)
    
class HobbiesView(TemplateView):
    template_name = "portfolio_app/hobbies.html"
    
class AboutmeView(TemplateView):
    template_name = "portfolio_app/aboutme.html"
    
class AnimeView(TemplateView):
    template_name = "portfolio_app/anime.html"

class GamesView(TemplateView):
    template_name = "portfolio_app/games.html"
    
class ProjectsView(TemplateView):
    template_name = "portfolio_app/projects.html"
    