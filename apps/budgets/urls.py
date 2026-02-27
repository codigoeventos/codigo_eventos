"""
URL configuration for Budgets app.
"""

from django.urls import path
from . import views

app_name = 'budgets'

urlpatterns = [
    path('', views.BudgetListView.as_view(), name='list'),
    path('create/', views.BudgetCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BudgetDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='delete'),
    path('<int:pk>/calculate-freight/', views.BudgetCalculateFreightView.as_view(), name='calculate-freight'),
    path('freight-preview/', views.BudgetFreightPreviewView.as_view(), name='freight-preview'),
    
    # Public approval URLs (no login required)
    path('approval/<uuid:token>/', views.PublicBudgetApprovalView.as_view(), name='public_approval'),
    path('approval/<uuid:token>/pdf/', views.PublicBudgetPDFView.as_view(), name='public_pdf'),
]
