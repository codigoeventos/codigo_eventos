"""
URL configuration for the Logistics / Freight app.
"""

from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    # Main configuration panel
    path('config/', views.FreightSettingsView.as_view(), name='config'),

    # Weight range CRUD
    path('weight-ranges/add/', views.WeightRangeCreateView.as_view(), name='weight-range-add'),
    path('weight-ranges/<int:pk>/edit/', views.WeightRangeUpdateView.as_view(), name='weight-range-edit'),
    path('weight-ranges/<int:pk>/delete/', views.WeightRangeDeleteView.as_view(), name='weight-range-delete'),

    # Volume range CRUD
    path('volume-ranges/add/', views.VolumeRangeCreateView.as_view(), name='volume-range-add'),
    path('volume-ranges/<int:pk>/edit/', views.VolumeRangeUpdateView.as_view(), name='volume-range-edit'),
    path('volume-ranges/<int:pk>/delete/', views.VolumeRangeDeleteView.as_view(), name='volume-range-delete'),

    # Urgency multiplier CRUD
    path('urgency/add/', views.UrgencyCreateView.as_view(), name='urgency-add'),
    path('urgency/<int:pk>/edit/', views.UrgencyUpdateView.as_view(), name='urgency-edit'),
    path('urgency/<int:pk>/delete/', views.UrgencyDeleteView.as_view(), name='urgency-delete'),
]
