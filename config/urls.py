"""
URL Configuration for Event Management System.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Root redirect to dashboard
    path('', RedirectView.as_view(pattern_name='dashboard:home', permanent=False)),
    
    # Apps
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('clients/', include('apps.clients.urls')),
    path('events/', include('apps.events.urls')),
    path('projects/', include('apps.projects.urls')),
    path('budgets/', include('apps.budgets.urls')),
    path('service-orders/', include('apps.service_orders.urls')),
    path('technical-visits/', include('apps.technical_visits.urls')),
    path('contractors/', include('apps.contractors.urls')),
    
    # TODO: Add URLs for other apps as they are developed
    # path('documents/', include('apps.documents.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Customize admin site
admin.site.site_header = "Sistema de Gestão de Eventos"
admin.site.site_title = "Gestão de Eventos"
admin.site.index_title = "Painel de Administração"
