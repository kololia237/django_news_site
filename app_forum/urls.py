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

from app_forum import views

urlpatterns = [

    path('', views.index, name='forum-index'),

    re_path(r'^(\d+)/$', views.forum, name='forum-detail'),
    path('newforum/', views.new_forum, name='new-forum'),
    path('<int:pk>/update/', views.ForumUpdateView.as_view(), name='forum-update'),
    path('<int:pk>/delete/', views.ForumDeleteView.as_view(), name='forum-delete'),

    re_path(r'^topic/(\d+)/$', views.topic, name='topic-detail'),
    path('topic/<int:pk>/update/', views.TopicUpdateView.as_view(), name='topic-update'),
    path('topic/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic-delete'),
    re_path(r'newtopic/(\d+)/$', views.new_topic, name='new-topic'),

    re_path(r'^comment/(\d+)/$', views.topic, name='comment'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:id>/', views.topic, name='comment'),

    # re_path(r'^reply/(\d+)/$', views.reply, name='reply'),
    # path('reply/<int:pk>/update/', views.CommentUpdateView.as_view(), name='reply-update'),
    # path('reply/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='reply-delete'),
    # path('reply/<int:id>/', views.topic, name='reply'),
]
