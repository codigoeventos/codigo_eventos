"""
URL configuration for Service Orders app.
"""

from django.urls import path
from . import views

app_name = 'service_orders'

urlpatterns = [
    path('', views.ServiceOrderListView.as_view(), name='list'),
    path('create/', views.ServiceOrderCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ServiceOrderDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ServiceOrderUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ServiceOrderDeleteView.as_view(), name='delete'),
]
