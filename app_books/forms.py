from django import forms
from django.forms import ModelForm

from .models import *


class AuthorForm(ModelForm):
    name = forms.CharField(label='Введіть ім`я', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Введіть прізвище', widget=forms.TextInput(attrs={'class': 'form-control'}))
    biography = forms.CharField(label='Введіть біографію',
                                widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Authors
        fields = ('name', 'surname', 'biography', 'img')


class BookForm(ModelForm):
    title = forms.CharField(label='Введіть назву (ім`я)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Введіть анотацію',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    img_name = forms.CharField(label='Заголовок зображення', widget=forms.TextInput(attrs={'class': 'form-control'}))

    # rate = forms.IntegerField(label='Оцінка',
    #                           widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '5'}))

    class Meta:
        model = Books
        fields = ('title', 'description', 'book_author', 'img','img_name', 'genre')


class GenreForm(ModelForm):
    title = forms.CharField(label='Введіть назву жанру', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Введіть опис жанру', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Genres
        fields = ('title', 'description', 'img')


class TypeBooksForm(ModelForm):
    rate = forms.IntegerField(label='Оцінка',
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '5'}))

    class Meta:
        model = Books
        fields = ('rate', 'read_now', 'want_to_read', 'read_books')


class SortForm(forms.Form):
    sort = forms.ModelChoiceField(queryset=Books.objects.all())


class ReviewForm(ModelForm):
    title = forms.CharField(label='Введіть назву (ім`я)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Введіть анотацію',
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Reviews
        fields = ('title', 'description')
