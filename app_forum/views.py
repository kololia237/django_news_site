from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
# from django.core.context_processors import csrf
from django.template.context_processors import csrf
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView

from app_forum.forms import *
from app_forum.settings import *


def index(request):
    """Main listing."""
    forums = Forum.objects.all()
    forums = mk_paginator(request, forums, FORUM_PER_PAGE)
    context = {
        'forums': forums,
        'user': request.user
    }
    return render(request, 'app_forum/list.html', context)


def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


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


def forum(request, forum_id):
    """Listing of topics in a forum."""
    topics = Topic.objects.filter(forum=forum_id).order_by("-created")
    topics = mk_paginator(request, topics, FORUM_PER_PAGE)

    forum = get_object_or_404(Forum, pk=forum_id)

    return render(request, "app_forum/forum.html",
                  add_csrf(request, topics=topics, pk=forum_id, forum=forum))


def topic(request, topic_id):
    topics = Topic.objects.filter(pk=topic_id)
    form = CommentForm()
    comments = Comment.objects.filter(topic_id=topic_id).order_by("-id")
    comments = mk_paginator(request, comments, FORUM_COMMENTS_PER_PAGE)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            Comment.objects.create(body=request.POST.get('body'), creator=request.user,
                                   topic=Topic.objects.get(id=topic_id))
            return HttpResponseRedirect(reverse('topic-detail', args=topic_id))

    return render(request, "app_forum/topic.html", context={
        'form': form,
        'topics': topics,
        'comments': comments,
        'user': request.user,
    })


@login_required
def new_topic(request, forum_id):
    form = TopicForm()
    forum = get_object_or_404(Forum, pk=forum_id)

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            topic = Topic()
            topic.title = form.cleaned_data['title']
            topic.description = form.cleaned_data['description']
            topic.forum = forum
            topic.creator = request.user

            topic.save()

            return HttpResponseRedirect(reverse('forum-detail', args=(forum_id,)))
    context = {
        'form': form,
        'forum': forum,
    }
    return render(request, 'app_forum/new-topic.html', context)


class TopicUpdateView(UpdateView):
    model = Topic
    template_name = 'app_forum/update-topic.html'
    form_class = TopicForm


class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'app_forum/delete.html'
    success_url = '/forum/'


@login_required
def new_forum(request):
    error = ''
    if request.method == 'POST':
        form = TopicForm(request.POST)

        if form.is_valid():
            Forum.objects.create(title=request.POST.get('title'), description=request.POST.get('description'),
                                 creator=request.user)
            return redirect('forum-index')

    form = TopicForm()
    context = {
        'form': form,
        'author': request.user,
        'error': error
    }
    return render(request, 'app_forum/new-forum.html', context)


class ForumUpdateView(UpdateView):
    model = Forum
    template_name = 'app_forum/update-topic.html'
    form_class = TopicForm


class ForumDeleteView(DeleteView):
    model = Forum
    template_name = 'app_forum/delete.html'
    success_url = '/forum/'


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'app_forum/update-comment.html'
    form_class = CommentForm


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'app_forum/delete.html'
    success_url = '/forum/'
