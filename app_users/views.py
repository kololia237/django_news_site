from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app_articles.models import *
from app_articles.settings import *
from app_articles.utils import DataMixin
from app_books.models import *
from app_forum.views import *
from .forms import *


class LoginUser(DataMixin, LoginView):
    form_class = AuthForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Реєстрація")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')


def ajax_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)


def ajax_login(request):
    username = request.GET.get('username', None)
    password = request.GET.get('password', None)
    response = {
        'is_taken': {User.objects.filter(username__iexact=username).exists(),
                     User.objects.filter(password__iexact=password).exists()}
    }
    return JsonResponse(response)


def logout_view(request):
    logout(request)
    return redirect('login')


# contact_list = Articles.objects.order_by('-id').all()
# tasks = mk_paginator(request, contact_list, MAIN_TASKS_PER_PAGE)
# return render(request, 'app_articles/index.html', {'tasks': tasks, })
def UserDetailView(request, user_id):
    articles = Articles.objects.filter(author_article=user_id).order_by("-id")[:5]

    books_read_now = Books.objects.filter(read_now=user_id).order_by("-id")[:5]
    books_read_now_count = Books.objects.filter(read_now=user_id).count()

    books_want_to_read = Books.objects.filter(want_to_read=user_id).order_by("-id")[:5]
    books_want_to_read_count = Books.objects.filter(want_to_read=user_id).count()

    read_books = Books.objects.filter(read_books=user_id).order_by("-id")[:5]
    read_books_count = Books.objects.filter(read_books=user_id).count()

    top_5_read_books = Books.objects.filter(read_books=user_id).order_by("rate")[:5]

    articles = mk_paginator(request, articles, MAIN_TASKS_FOR_PROFILE_PER_PAGE)
    user = User.objects.get(pk=user_id)

    # if request.method == 'POST':
    #     form = ChangeUserStatusForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.save()
    #         return redirect('home')
    #
    # form = ChangeUserStatusForm()

    return render(request, "profile.html", context={
        # 'form': form,
        'articles': articles,
        'books_read_now': books_read_now,
        'books_want_to_read': books_want_to_read,
        'read_books': read_books,
        'top_5_read_books': top_5_read_books,
        'user': user,

        'books_read_now_count': books_read_now_count,
        'books_want_to_read_count': books_want_to_read_count,
        'read_books_count': read_books_count
    })


#################


def profile_statistics(request, user_id):
    read_books_count = Books.objects.filter(read_books=user_id).count()
    read_books_date = Books.objects.filter(read_books=user_id).order_by("date_updated")

    return render(request, "profile_statistics.html", context={
        'read_books_date': read_books_date,
        'read_books_count': read_books_count,
    })


class StatusUserUpdateView(UpdateView):
    model = User
    template_name = 'status.html'
    form_class = ChangeUserStatusForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Status'
        return context


# PROFILE UPDATE
class UserUpdateView(UpdateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редагування даних'
        return context


class ChangePassView(UpdateView):
    model = User
    template_name = 'change-pass.html'
    form_class = ChangePassUserForm
    success_url = '/'

    def form_valid(self, form):
        user = form.save()
        # user = User.objects.create(username=self.request.POST.get('username'), email=self.request.POST.get('email'),
        # password=self.request.POST.get('password1'))

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('home')
