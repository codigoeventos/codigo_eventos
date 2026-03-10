"""
URL patterns for dashboard app.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('project-totals/', views.ProjectTotalsView.as_view(), name='project_totals'),
]
