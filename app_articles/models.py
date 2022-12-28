from django.contrib.auth.models import User
from django.db import models

from app_books.models import Books
from .validators import validate_file_extension


class Categories(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=20)
    description = models.TextField(verbose_name='Опис', blank=True)
    img = models.FileField(verbose_name='Картинка', default=None, upload_to="category_images/%Y/%m/%d/",
                           validators=[validate_file_extension])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/tasks/category/{self.id}/'

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Articles(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=50)
    description = models.TextField(verbose_name='Опис')
    quote = models.TextField(verbose_name='Цитата', default='', blank=True)
    biography = models.TextField(verbose_name='Біографія', default='')
    full_name = models.CharField(verbose_name='Повне ім`я', default='', max_length=50)
    related_books = models.CharField(verbose_name='Назва', max_length=50, default='')
    img = models.FileField(verbose_name='Картинка', default=None, upload_to="articles_images/%Y/%m/%d/",
                           validators=[validate_file_extension])
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(verbose_name='к-сть переглядів', default=0)
    connected_book = models.ForeignKey(Books, verbose_name='Пов`язана книжка', blank=True, default=None, null=True,
                                       on_delete=models.PROTECT, related_name='book')
    # через панель адміністратора усі можливі автори
    author_article = models.ForeignKey(User, verbose_name='Автор статті', default=None, null=True,
                                       on_delete=models.PROTECT, related_name='author')
    category = models.ForeignKey(Categories, verbose_name="Категорія", default='', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/articles/{self.id}'

    # def short(self):
    #     return u"%s" % self.title
    #
    # short.allow_tags = True

    class Meta:
        ordering = ['-id']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'


class HomePage(models.Model):
    welcome_text = models.TextField(verbose_name='welcome_text')
    help_text = models.TextField(verbose_name='Допомога')

    def __str__(self):
        return self.welcome_text

    def get_absolute_url(self):
        return '/'

    class Meta:
        verbose_name = 'Головна сторінка'
        verbose_name_plural = 'Головна сторінка'
