"""
URL configuration for temp_project project.

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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings # Import settings
from django.conf.urls.static import static # For serving media files in development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')), # <--- Crucial!
    path('login/', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Your app's URLs. Keep them above the CMS URLs.
    path('', include('books.urls')), # This will now be superseded for CMS pages

    # CMS URLs (MUST BE LAST!)
    path('', include('cms.urls')),

    # Add includes for any other apps you discovered in your 'ls' output
    # For example, if 'abdrushin_books_sales' is an app:
    # path('sales/', include('abdrushin_books_sales.urls')),
    # If 'backend' is an app:
    # path('api/', include('backend.urls')),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
