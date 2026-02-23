"""
URL configuration for Projects app.
"""

from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('create/', views.ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='delete'),
    # Project files
    path('<int:project_pk>/files/upload/', views.ProjectFileCreateView.as_view(), name='file_upload'),
    path('files/<int:pk>/delete/', views.ProjectFileDeleteView.as_view(), name='file_delete'),
]
