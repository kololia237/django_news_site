from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

from app_articles.settings import *
from app_books.models import *
from .forms import *
from .utils import *


def home(request):
    categories = Categories.objects.order_by('-id')[:5]
    articles = Articles.objects.order_by('-id')[:5]
    genres = Genres.objects.order_by('-id')[:5]
    books = Books.objects.order_by('-id')[:5]

    return render(request, 'home.html',
                  {'home': home, 'articles': articles, 'categories': categories, 'genres': genres, 'books': books})


def gallery(request):
    articles = Articles.objects.order_by('-id')[:3]  # [:1]

    return render(request, 'gallery.html', {'articles': articles})


def statistics(request):
    return render(request, 'statistics.html')


def index(request):
    contact_list = Articles.objects.order_by('-id').all()
    articles = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
    return render(request, 'app_articles/index.html', {'articles': articles})


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


def create(request):
    error = ''

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_article = request.user

            post.save()
            # Articles.objects.create(title=request.POST.get('title'), desc=request.POST.get('desc'),
            #                     quote=request.POST.get('quote'), biography=request.POST.get('biography'),
            #                     img=request.FILES.get('img'), author=request.user,
            #                     full_name=request.POST.get('full_name'),
            #                     category=Categories.objects.get(id=request.POST.get('category')))
            return redirect('articles')
        else:
            print("ERROR!!!\nCAN NOT CREATE ARTICLE!'")
            error = 'ERROR!!!\nCAN NOT CREATE ARTICLE!'

    form = ArticleForm()
    context = {
        'form': form,
        'author': request.user,
        'error': error,
        'title': 'Створити статтю'
    }
    return render(request, 'app_articles/create.html', context)


class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'app_articles/article_details.html'
    context_object_name = 'article'

    def get_object(self, **kwargs):
        aw = Articles.objects.get(id=self.kwargs['pk'])
        aw.views_count += 1
        aw.save()
        return Articles.objects.get(id=self.kwargs['pk'])


class ArticleUpdateView(UpdateView):
    model = Articles
    template_name = 'app_articles/create.html'
    form_class = ArticleForm


class ArticleDeleteView(DeleteView):
    model = Articles
    template_name = 'app_articles/delete.html'
    success_url = '/articles/'


class SearchResultsView(ListView):
    model = Articles
    template_name = 'app_articles/search_articles.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            articles = Articles.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(quote__icontains=query) |
                Q(biography__icontains=query) |
                Q(full_name__icontains=query)
            )
            return articles
        else:
            articles = Articles.objects.all()
            return articles


class UpdateHomePageView(UpdateView):
    model = HomePage
    template_name = 'update_home_page.html'
    form_class = UpdateHomePageForm


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.save()
            return redirect('home')

    form = CategoryForm()
    context = {
        'form': form,
        'title': 'Створити категорію'
    }
    return render(request, 'app_articles/create.html', context)


def CategoryDetailView(request, category_id):
    articles = Articles.objects.filter(category=category_id).order_by("-id")
    articles = mk_paginator(request, articles, MAIN_TASKS_PER_PAGE)
    category = Categories.objects.get(pk=category_id)

    return render(request, "app_articles/category_details.html", context={
        'articles': articles,
        'category': category,
    })


class CategoryUpdateView(UpdateView):
    model = Categories
    template_name = 'app_articles/create.html'
    form_class = CategoryForm


class CategoryDeleteView(DeleteView):
    model = Categories
    template_name = 'app_articles/delete.html'
    success_url = '/s/'
