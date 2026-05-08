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
    path('item-descriptions/', views.ItemDescriptionListCreateView.as_view(), name='item-descriptions'),
    path('item-descriptions/<int:pk>/', views.ItemDescriptionDetailView.as_view(), name='item-descriptions-detail'),
    path('payment-info-templates/', views.PaymentInfoTemplateListCreateView.as_view(), name='payment-info-templates'),
    path('payment-info-templates/<int:pk>/', views.PaymentInfoTemplateDetailView.as_view(), name='payment-info-templates-detail'),
    
    # Notifications
    path('notifications/', views.NotificationsView.as_view(), name='notifications'),

    # Version history
    path('<int:pk>/versions/', views.BudgetVersionListView.as_view(), name='version-list'),
    path('<int:pk>/versions/<int:version_id>/', views.BudgetVersionDetailView.as_view(), name='version-detail'),
    path('<int:pk>/versions/<int:version_id>/restore/', views.BudgetVersionRestoreView.as_view(), name='version-restore'),
    path('<int:pk>/versions/<int:version_id>/preview/', views.BudgetVersionPublicPreviewView.as_view(), name='version-preview'),

    # Public approval URLs (no login required)
    path('approval/<uuid:token>/', views.PublicBudgetApprovalView.as_view(), name='public_approval'),
    path('approval/<uuid:token>/pdf/', views.PublicBudgetPDFView.as_view(), name='public_pdf'),
]
