"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from app_articles import views
from app_articles.views import *

# в файлі view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('gallery', views.gallery, name='gallery'),
    path('statistics', views.statistics, name='statistics'),

    path('articles/', include('app_articles.urls')),
    path('users/', include('app_users.urls')),
    path('forum/', include('app_forum.urls')),
    path('books/', include('app_books.urls')),

    path('search', SearchResultsView.as_view(), name='search'),
    path('update_home_page/<int:pk>', UpdateHomePageView.as_view(), name='update_home_page'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
