"""
URL configuration for ART app.
"""

from django.urls import path
from . import views

app_name = 'art'

urlpatterns = [
    path('budget/<int:budget_pk>/generate/', views.ARTGenerateView.as_view(), name='generate'),
    path('<int:pk>/', views.ARTDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ARTUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ARTDeleteView.as_view(), name='delete'),
    path('public/<uuid:token>/', views.PublicARTView.as_view(), name='public'),
]
