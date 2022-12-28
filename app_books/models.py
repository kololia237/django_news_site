from django.contrib.auth.models import User
from django.db import models

from app_articles.validators import validate_file_extension


# Create your models here.


class Authors(models.Model):
    name = models.CharField(verbose_name='Ім`я', max_length=50)
    surname = models.CharField(verbose_name='Призвіще', max_length=50)
    biography = models.TextField(verbose_name='Біографія', blank=True)
    creator = models.ForeignKey(User, verbose_name="Створювач", null=False, on_delete=models.CASCADE, default=None)
    img = models.FileField(verbose_name='Фото автора',
                           default=None,
                           upload_to="author_images/%Y/%m/%d/",
                           validators=[validate_file_extension])

    def __str__(self):
        return self.name + " " + self.surname

    def get_absolute_url(self):
        return f'/books/author/{self.id}/'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автори'


class Genres(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=50)
    description = models.TextField(verbose_name='Опис', blank=True)
    img = models.FileField(verbose_name='Картинка', default=None, upload_to="genres_images/%Y/%m/%d/",
                           validators=[validate_file_extension])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/books/genre/{self.id}'

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанри'


class Books(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=50)
    description = models.TextField(verbose_name='Опис')
    rate = models.IntegerField(verbose_name='Оцінка', default=0, blank=True, null=True)
    img = models.FileField(verbose_name='Картинка', default="![](../static/img/book_default.png)",
                           upload_to="books_images/%Y/%m/%d/", blank=True, null=True)
    img_name = models.CharField(verbose_name='Нзва картинки', default=" ", max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # views_count = models.IntegerField(verbose_name='к-сть переглядів', default=0, blank=True, null=True)
    creator = models.ForeignKey(User, verbose_name="Додав книжку", default='', on_delete=models.PROTECT)
    book_author = models.ForeignKey(Authors, verbose_name="Автор", default='', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, verbose_name="Жанр", default='', on_delete=models.CASCADE)

    read_now = models.ManyToManyField(User, verbose_name="Читаю зараз", blank=True, related_name='read_now')
    want_to_read = models.ManyToManyField(User, verbose_name="Хочу прочитати", blank=True, related_name='want_to_read')
    read_books = models.ManyToManyField(User, verbose_name="Прочитано", blank=True, related_name='read_books')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/books/{self.id}'

    def short(self):
        return u"%s" % self.title

    short.allow_tags = True

    class Meta:
        ordering = ['-id']
        verbose_name = 'Книжка'
        verbose_name_plural = 'Книжки'


# class Rates(models.Model):
#     value = models.SmallIntegerField(verbose_name='Оцінка користувача', blank=True, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     book = models.ForeignKey(Books, on_delete=models.CASCADE)
#     voted_on = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         ordering = ['-id']
#         verbose_name = 'Оцінка'
#         verbose_name_plural = 'Оцінки'

class Reviews(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=150)
    description = models.TextField(verbose_name='Основна частина')
    book = models.ForeignKey(Books, verbose_name='Пов`язана книжка', blank=True, default=None, null=True,
                             on_delete=models.CASCADE, related_name='book_review')
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name="Автор рецензії", null=False, on_delete=models.CASCADE, default=None)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s - %s" % (self.creator, self.book.title)

    def short(self):
        return u"%s - %s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецензія'
        verbose_name_plural = 'Рецензії'


class CommentReview(models.Model):
    body = models.TextField(verbose_name="Коментар до рецензії", max_length=1000, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, verbose_name="Автор коментаря до рецензії", null=False, on_delete=models.CASCADE,
                                default=None)
    updated = models.DateTimeField(auto_now=True)
    review = models.ForeignKey(Reviews, verbose_name="Рецензія", on_delete=models.CASCADE)

    def __str__(self):
        return u"%s - %s - %s" % (self.creator, self.body, self.review.title)

    def short(self):
        return u"%s - %s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'

    def get_absolute_url(self):
        return f'/books/review/{self.review.id}'
