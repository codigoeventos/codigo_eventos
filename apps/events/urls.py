"""
URL configuration for Events app.
"""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('create/', views.EventCreateView.as_view(), name='create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='delete'),

    # Contractor assignment
    path('<int:pk>/contractors/assign/', views.ContractorAssignView.as_view(), name='contractor_assign'),
    path('<int:pk>/contractors/<int:assignment_pk>/edit/', views.ContractorAssignEditView.as_view(), name='contractor_assign_edit'),
    path('<int:pk>/contractors/<int:assignment_pk>/remove/', views.ContractorAssignRemoveView.as_view(), name='contractor_assign_remove'),
    path('api/contractor-members/', views.ContractorMembersJSONView.as_view(), name='contractor_members_json'),
]
