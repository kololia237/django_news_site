from django.contrib.auth.models import User
from django.db import models


# from django.contrib import admin


# from django.utils.translation import ugettext_lazy as _


class Forum(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=60, blank=False)
    description = models.TextField(verbose_name="Опис", blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name="Автор", null=False, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/forum/'

    class Meta:
        verbose_name = 'Форум'
        verbose_name_plural = 'Форуми'

    def num_comments(self):
        return sum([t.num_comments() for t in self.topic_set.all()])

    def last_comment(self):
        if self.topic_set.count():
            last = None
            for t in self.topic_set.all():
                l = t.last_comment()
                if l:
                    if not last:
                        last = l
                    elif l.created > last.created:
                        last = l
            return last


class Topic(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=60, blank=False)
    description = models.TextField(verbose_name="Опис", max_length=10000, blank=False, null=True)
    forum = models.ForeignKey(Forum, verbose_name="Форум", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name="Автор", null=False, on_delete=models.PROTECT, default=None)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Обговорення'
        verbose_name_plural = 'Обговорення'

    def num_comments(self):
        return self.comment_set.count()

    def num_comms(self):
        return max(0, self.comment_set.count())

    def last_comment(self):
        if self.comment_set.count():
            return self.comment_set.order_by("created")[0]

    def __str__(self):
        return str(self.creator) + " - " + self.title

    def get_absolute_url(self):
        return f'/forum/topic/{self.id}/'


class Comment(models.Model):
    body = models.TextField(verbose_name="Коментар", max_length=1000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name="Автор", null=False, on_delete=models.CASCADE, default=None)
    updated = models.DateTimeField(auto_now=True)
    topic = models.ForeignKey(Topic, verbose_name="Обговорення", on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s - %s" % (self.creator, self.body, self.topic.title)

    def short(self):
        return u"%s - %s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def get_absolute_url(self):
        return f'/forum/topic/{self.topic.id}'


# class ReplyForComment(models.Model):
#     text = models.TextField(verbose_name="Текст", max_length=10000, blank=False)
#     created = models.DateTimeField(auto_now_add=True)
#     comment = models.ForeignKey(Comment, verbose_name="коментар", on_delete=models.CASCADE)
#     creator = models.ForeignKey(User, verbose_name="Автор відповіді на коментар", null=False, on_delete=models.CASCADE,
#                                 default=None)
#     updated = models.DateTimeField(auto_now=True)
#     user_ip = models.GenericIPAddressField(verbose_name="IP адреса користувача", blank=True, null=True)
#
#     def __str__(self):
#         return u"%s - %s - %s" % (self.creator, self.text, self.comment.title)
#
#     def short(self):
#         return u"%s - %s\n%s" % (self.creator, self.text, self.created.strftime("%b %d, %I:%M %p"))
#
#     short.allow_tags = True
#
#     class Meta:
#         verbose_name = 'Відповідь на коментар'
#         verbose_name_plural = 'Відповіді на коментарі'
#
#     def get_absolute_url(self):
#         # return f'/{self.id}'
#         return f'/forum/topic/{self.comment.topic.id}'


class ProfaneWord(models.Model):
    word = models.CharField(verbose_name="", max_length=60)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Заборонене слово'
        verbose_name_plural = 'Заборонені слова'
