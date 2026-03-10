"""
URL patterns for dashboard app.
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='home'),
    path('financeiro/', views.FinancialDashboardView.as_view(), name='financial'),
]
