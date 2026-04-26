# portfolio_app/urls.py
"""
URL configuration for portfolio_app.

Defines URL patterns for all portfolio pages including home, about, projects,
hobbies, anime, games, and contact functionality.
"""
# ----------------------------------------------------------------------------------------------------

from django.urls import path
from . import views
from accounts.views import contact_view

app_name = 'portfolio_app'

urlpatterns = [
    path('',
         views.home_view,
         name='home'),
    
    path('contact/',
         contact_view,
         name='contact'),
    
    path('hobbies/', 
         views.HobbiesView.as_view(), 
         name='hobbies'),
    
    path('aboutme/', 
         views.AboutmeView.as_view(), 
         name='aboutme'),
    
    path('hobbies/anime/', 
         views.AnimeView.as_view(), 
         name='anime'),
    
    path('hobbies/games/', 
         views.GamesView.as_view(), 
         name='games'),
    
    path('portfolio/projects/', 
         views.ProjectsView.as_view(), 
         name='projects'),
]
