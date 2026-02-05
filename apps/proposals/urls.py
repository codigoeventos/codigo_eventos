"""
URL configuration for Proposals app.
"""

from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('', views.ProposalListView.as_view(), name='list'),
    path('create/', views.ProposalCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProposalDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProposalUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ProposalDeleteView.as_view(), name='delete'),
]
