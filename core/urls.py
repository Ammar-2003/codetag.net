"""
URL configuration for core project.

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
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from app.blog.sitemaps import BlogSitemap
from app.blog.views import robots_txt

sitemaps_dict = {
    'blogs': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.home.urls')),
    path('blog/', include('app.blog.urls')),
    path('accounts/', include('app.accounts.urls')),
    path('pages/', include('app.pages.urls')),
    path('dashboard/', include('app.dashboard.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_dict}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
