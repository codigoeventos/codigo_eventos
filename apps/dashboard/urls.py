"""
URL patterns for dashboard app.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('proposal-totals/', views.ProposalTotalsView.as_view(), name='proposal_totals'),
]
