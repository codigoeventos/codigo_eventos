"""
URL configuration for Contractors app.
"""

from django.urls import path
from . import views

app_name = 'contractors'

urlpatterns = [
    # Report
    path('doc-report/', views.DocumentationReportView.as_view(), name='doc_report'),

    # API endpoint
    path('api/cnpj-lookup/', views.CNPJLookupView.as_view(), name='cnpj_lookup'),
    
    # Contractor CRUD
    path('', views.ContractorListView.as_view(), name='list'),
    path('create/', views.ContractorCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ContractorDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ContractorUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ContractorDeleteView.as_view(), name='delete'),

    # Member CRUD (nested under contractor)
    path('<int:contractor_pk>/members/add/', views.MemberCreateView.as_view(), name='member_create'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('members/<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member_edit'),
    path('members/<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),
]
