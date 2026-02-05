"""
URL configuration for Technical Visits app.
"""

from django.urls import path
from . import views

app_name = 'technical_visits'

urlpatterns = [
    path('', views.TechnicalVisitListView.as_view(), name='list'),
    path('create/', views.TechnicalVisitCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TechnicalVisitDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TechnicalVisitUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TechnicalVisitDeleteView.as_view(), name='delete'),
]
