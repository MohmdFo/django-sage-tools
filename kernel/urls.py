"""
URL configuration for kernel project.

This configuration provides testing endpoints for the django-sage-tools package.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

# Basic URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    # Example test views for sage_tools components
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    # You can add test URLs for sage_tools components here
    # path('test/', include('sage_tools.urls')),  # If you create URLs in sage_tools
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Admin site customization
admin.site.site_header = "Django Sage Tools Development"
admin.site.site_title = "Sage Tools Admin"
admin.site.index_title = "Welcome to Sage Tools Administration"
