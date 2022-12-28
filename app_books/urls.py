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

from app_books import views
from app_books.views import *

# в файлі view
urlpatterns = [
    path('', views.index_books, name='books'),
    path('authors', views.index_authors, name='authors'),
    path('add_author', views.add_author, name='add-author'),
    re_path(r'^author/(\d+)/$', views.author_p, name='author-detail'),
    path('author/<int:pk>/update', views.AuthorUpdateView.as_view(), name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),

    # STATISTICS
    path('old', views.index_books_old, name='books_old'),
    path('title', views.index_books_title, name='books_title'),
    path('book_author', views.index_books_book_author, name='books_book_author'),
    path('rate', views.index_books_rate, name='books_rate'),
    # STATISTICS

    path('add', views.add_book, name='add-book'),
    path('<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^(\d+)/articles$', connected_book, name='connected_book'),
    path('<int:pk>/update', views.BookUpdateView.as_view(), name='book-update'),
    path('<int:pk>/delete', views.BookDeleteView.as_view(), name='book-delete'),

    # STATISTICS
    re_path(r'^read_now/(\d+)/$', read_now, name='read_now'),
    re_path(r'^want_to_read/(\d+)/$', want_to_read, name='want_to_read'),
    re_path(r'^read_books/(\d+)/$', read_books, name='read_books'),

    re_path(r'^read_books/(\d+)/old$', read_books_old, name='read_books_old'),
    re_path(r'^read_books/(\d+)/title$', read_books_title, name='read_books_title'),
    re_path(r'^read_books/(\d+)/book_author$', read_books_book_author, name='read_books_book_author'),
    re_path(r'^read_books/(\d+)/rate$', read_books_rate, name='read_books_rate'),

    re_path(r'^read_now/(\d+)/old$', read_now_old, name='read_now_old'),
    re_path(r'^read_now/(\d+)/title$', read_now_title, name='read_now_title'),
    re_path(r'^read_now/(\d+)/book_author$', read_now_book_author, name='read_now_book_author'),
    re_path(r'^read_now/(\d+)/rate$', read_now_rate, name='read_now_rate'),

    re_path(r'^want_to_read/(\d+)/old$', want_to_read_old, name='want_to_read_old'),
    re_path(r'^want_to_read/(\d+)/title$', want_to_read_title, name='want_to_read_title'),
    re_path(r'^want_to_read/(\d+)/book_author$', want_to_read_book_author, name='want_to_read_book_author'),
    re_path(r'^want_to_read/(\d+)/rate$', want_to_read_rate, name='want_to_read_rate'),

    # STATISTICS

    path('genres', views.index_genres, name='genres'),
    path('create-genre', views.add_genre, name='create-genre'),
    path('genre/<int:pk>/update', views.GenreUpdateView.as_view(), name='update-genre'),
    path('genre/<int:pk>/delete', views.GenreDeleteView.as_view(), name='delete-genre'),
    re_path(r'^genre/(\d+)/$', views.GenreDetailView, name='genre-detail'),

    # re_path(r'^(\d+)/reviews$', views.review, name='reviews'),
    # re_path(r'newreview/(\d+)/$', views.new_review, name='new_review'),

    re_path(r'^(\d+)/reviews$', all_reviews, name='all_reviews'),
    re_path(r'^review/(\d+)/$', views.review, name='reviews'),
    re_path(r'newreview/(\d+)/$', views.new_review, name='new_review'),
    path('review/<int:pk>/update', views.ReviewUpdateView.as_view(), name='review-update'),
    path('review/<int:pk>/delete', views.ReviewDeleteView.as_view(), name='review-delete'),

    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]
