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
from django.urls import path, re_path

from app_articles import views

# в файлі view
urlpatterns = [
    path('', views.index, name='articles'),

    path('create', views.create, name='create'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('<int:pk>/update', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<int:pk>/delete', views.ArticleDeleteView.as_view(), name='article-delete'),

    path('create-category', views.create_category, name='create-category'),
    path('category/<int:pk>/update', views.CategoryUpdateView.as_view(), name='update-category'),
    path('category/<int:pk>/delete', views.CategoryDeleteView.as_view(), name='delete-category'),

    re_path(r'^category/(\d+)/$', views.CategoryDetailView, name='category-detail'),

]
