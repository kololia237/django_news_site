from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView, ListView

from app_articles.models import Articles
from app_books.settings import *
from app_forum.forms import CommentForm
from app_forum.views import add_csrf
from .forms import *
from .utils import *


def index_genres(request):
    contact_list = Genres.objects.order_by('-id').all()
    genres = mk_paginator(request, contact_list, BOOKS_PER_PAGE)
    return render(request, 'app_books/all_genres.html', {'genres': genres})


def index_authors(request):
    contact_list = Authors.objects.order_by('name', 'surname').all()
    authors = mk_paginator(request, contact_list, BOOKS_PER_PAGE)
    return render(request, 'app_books/author/all_authors.html', {'authors': authors})


# Author
def author_p(request, author_id):
    author = Authors.objects.get(pk=author_id)
    books = Books.objects.filter(book_author=author_id).order_by("-id")

    return render(request, "app_books/author/author_profile.html", context={
        'author': author,
        'books': books
    })


def add_author(request):
    error = ''

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user

            post.save()
            return redirect('authors')
        else:
            print("ERROR!!!\nCAN NOT ADD BOOK!'")
            error = 'ERROR!!!\nCAN NOT ADD BOOK!'

    form = AuthorForm()
    context = {
        'form': form,
        'author': request.user,
        'error': error,
        'title': 'Додати автора'
    }
    return render(request, 'app_books/add_book.html', context)


class AuthorUpdateView(UpdateView):
    model = Authors
    template_name = 'app_books/add_book.html'
    form_class = AuthorForm


class AuthorDeleteView(DeleteView):
    model = Authors
    template_name = 'app_books/delete.html'
    success_url = '/books/'


# STATISTICS
def index_books(request):
    # contact_list = Books.objects.order_by('-id').all()
    # books = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)

    books = Books.objects.order_by('-date_created').all()
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    return render(request, 'app_books/index.html', {'books': books})


def index_books_old(request):
    # contact_list = Books.objects.order_by('-id').all()
    # books = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
    books = Books.objects.order_by('date_created').all()
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    return render(request, 'app_books/index.html', {'books': books})


def index_books_title(request):
    # contact_list = Books.objects.order_by('-id').all()
    # books = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
    books = Books.objects.order_by('title').all()
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    return render(request, 'app_books/index.html', {'books': books})


def index_books_book_author(request):
    # contact_list = Books.objects.order_by('-id').all()
    # books = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
    books = Books.objects.order_by('book_author').all()
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    return render(request, 'app_books/index.html', {'books': books})


def index_books_rate(request):
    # contact_list = Books.objects.order_by('-id').all()
    # books = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
    books = Books.objects.order_by('-rate').all()
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    return render(request, 'app_books/index.html', {'books': books})


def read_now(request, user_id):
    books_read_now = Books.objects.filter(read_now=user_id).order_by("-id")
    books_read_now = mk_paginator(request, books_read_now, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_now.html", context={
        'books_read_now': books_read_now,
        'user': user,
    })


def read_now_old(request, user_id):
    books_read_now = Books.objects.filter(read_now=user_id).order_by("id")
    books_read_now = mk_paginator(request, books_read_now, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_now.html", context={
        'books_read_now': books_read_now,
        'user': user,
    })


def read_now_title(request, user_id):
    books_read_now = Books.objects.filter(read_now=user_id).order_by("title")
    books_read_now = mk_paginator(request, books_read_now, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_now.html", context={
        'books_read_now': books_read_now,
        'user': user,
    })


def read_now_book_author(request, user_id):
    books_read_now = Books.objects.filter(read_now=user_id).order_by("book_author")
    books_read_now = mk_paginator(request, books_read_now, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_now.html", context={
        'books_read_now': books_read_now,
        'user': user,
    })


def read_now_rate(request, user_id):
    books_read_now = Books.objects.filter(read_now=user_id).order_by("-rate")
    books_read_now = mk_paginator(request, books_read_now, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'books_read_now': books_read_now,
        'user': user,
    })


def want_to_read(request, user_id):
    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("-id")
    books_want_to_read = mk_paginator(request, books_want_to_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/want_to_read.html", context={
        'books_want_to_read': books_want_to_read,
        'user': user,
    })


def want_to_read_old(request, user_id):
    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("-id")
    books_want_to_read = mk_paginator(request, books_want_to_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/want_to_read.html", context={
        'books_want_to_read': books_want_to_read,
        'user': user,
    })


def want_to_read_title(request, user_id):
    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("title")
    books_want_to_read = mk_paginator(request, books_want_to_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/want_to_read.html", context={
        'books_want_to_read': books_want_to_read,
        'user': user,
    })


def want_to_read_book_author(request, user_id):
    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("book_author")
    books_want_to_read = mk_paginator(request, books_want_to_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/want_to_read.html", context={
        'books_want_to_read': books_want_to_read,
        'user': user,
    })


def want_to_read_rate(request, user_id):
    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("-rate")
    books_want_to_read = mk_paginator(request, books_want_to_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/want_to_read.html", context={
        'books_want_to_read': books_want_to_read,
        'user': user,
    })


def read_books(request, user_id):
    books_read = Books.objects.filter(read_books=user_id).order_by("-id")
    books_read = mk_paginator(request, books_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'read_books': books_read,
        'user': user,
    })


def read_books_old(request, user_id):
    books_read = Books.objects.filter(read_books=user_id).order_by("id")
    books_read = mk_paginator(request, books_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'read_books': books_read,
        'user': user,
    })


def read_books_title(request, user_id):
    books_read = Books.objects.filter(read_books=user_id).order_by("title")
    books_read = mk_paginator(request, books_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'read_books': books_read,
        'user': user,
    })


def read_books_book_author(request, user_id):
    books_read = Books.objects.filter(read_books=user_id).order_by("book_author")
    books_read = mk_paginator(request, books_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'read_books': books_read,
        'user': user,
    })


def read_books_rate(request, user_id):
    books_read = Books.objects.filter(read_books=user_id).order_by("-rate")
    books_read = mk_paginator(request, books_read, BOOKS_PER_PAGE)
    user = User.objects.get(pk=user_id)

    return render(request, "app_books/statistics/read_books.html", context={
        'read_books': books_read,
        'user': user,
    })


def mk_paginator(request, items, num_items):
    """Create and return a paginator."""
    paginator = Paginator(items, num_items)
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError:
        page = 1

    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items


def add_book(request):
    error = ''

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user

            post.save()
            return redirect('books')
        else:
            print("ERROR!!!\nCAN NOT ADD BOOK!'")
            error = 'ERROR!!!\nCAN NOT ADD BOOK!'

    form = BookForm()
    context = {
        'form': form,
        'author': request.user,
        'error': error,
        'title': 'Додати книгу'
    }
    return render(request, 'app_books/add_book.html', context)


class BookDetailView(UpdateView):
    model = Books
    template_name = 'app_books/book_details.html'
    context_object_name = 'book'
    form_class = TypeBooksForm


def connected_book(request, book_id):
    articles = Articles.objects.filter(connected_book=book_id).order_by('-id').all()
    return render(request, 'app_articles/index.html', {'articles': articles})


class BookUpdateView(UpdateView):
    model = Books
    template_name = 'app_books/add_book.html'
    form_class = BookForm


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'app_books/delete.html'
    success_url = '/books/'


class SearchResultsView(ListView):
    model = Books
    template_name = 'app_books/search_book.html'

    def get_queryset(self):  # новый
        query = self.request.GET.get('q', '')
        if query:
            books = Books.objects.filter(
                Q(title__icontains=query) |
                Q(quote__icontains=query) |
                Q(biography__icontains=query) |
                Q(full_name__icontains=query)
            )
            return books
        else:
            books = Books.objects.all()
            return books


# class UpdateHomePageView(UpdateView):
#     model = HomePage
#     template_name = 'update_home_page.html'
#     form_class = UpdateHomePageForm


def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            return redirect('home')

    form = GenreForm()
    context = {
        'form': form,
        'title': 'Додати жанр'
    }
    return render(request, 'app_books/add_book.html', context)


def GenreDetailView(request, genre_id):
    books = Books.objects.filter(genre=genre_id).order_by("-id")
    books = mk_paginator(request, books, BOOKS_PER_PAGE)
    genre = Genres.objects.get(pk=genre_id)

    return render(request, "app_books/genre_details.html", context={
        'books': books,
        'genre': genre,
    })


class GenreUpdateView(UpdateView):
    model = Genres
    template_name = 'app_books/add_book.html'
    form_class = GenreForm


class GenreDeleteView(DeleteView):
    model = Genres
    template_name = 'app_books/delete.html'
    success_url = '/books/genres'


def all_reviews(request, book_id):
    """Listing of topics in a forum."""
    reviews = Reviews.objects.filter(book=book_id).order_by("-created")
    reviews = mk_paginator(request, reviews, REVIEWS_PER_PAGE)

    book = get_object_or_404(Books, pk=book_id)

    return render(request, "app_books/all_reviews.html",
                  add_csrf(request, reviews=reviews, pk=book_id, book=book))


def review(request, review_id):
    reviews = Reviews.objects.filter(pk=review_id)
    form = CommentForm()
    comments = CommentReview.objects.filter(review_id=review_id).order_by("-id")
    comments = mk_paginator(request, comments, REVIEWS_COMMENTS_PER_PAGE)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            CommentReview.objects.create(body=request.POST.get('body'), creator=request.user,
                                         review=Reviews.objects.get(id=review_id))
            return HttpResponseRedirect(reverse('reviews', args=review_id))

    return render(request, "app_books/review.html", context={
        'form': form,
        'reviews': reviews,
        'comments': comments,
        'user': request.user,
    })


@login_required
def new_review(request, book_id):
    form = ReviewForm()
    book = get_object_or_404(Books, pk=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.book = book
            post.save()

            return HttpResponseRedirect(reverse('book-detail', args=(book_id,)))
    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'app_books/new_review.html', context)


class ReviewUpdateView(UpdateView):
    model = Reviews
    template_name = 'app_books/add_book.html'
    form_class = ReviewForm


class ReviewDeleteView(DeleteView):
    model = Reviews
    template_name = 'app_books/delete.html'
    success_url = '/books/genres'


class CommentUpdateView(UpdateView):
    model = CommentReview
    template_name = 'app_forum/update-comment.html'
    form_class = CommentForm


class CommentDeleteView(DeleteView):
    model = CommentReview
    template_name = 'app_forum/delete.html'
    success_url = '/books'
