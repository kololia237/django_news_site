from django import forms
from django.forms import ModelForm, Textarea

from .models import *


class ArticleForm(ModelForm):
    title = forms.CharField(label='Введіть назву (ім`я)', widget=forms.TextInput(attrs={'class': 'form-control'}))
    full_name = forms.CharField(label='Введіть повну назву (ім`я)',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Введіть опис', widget=forms.Textarea(attrs={'class': 'form-control'}))
    quote = forms.CharField(label='Введіть цитату', widget=forms.Textarea(attrs={'class': 'form-control'}))
    biography = forms.CharField(label='Введіть біографію', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Articles
        fields = ('title', 'full_name', 'description', 'quote', 'biography', 'img', 'category', 'connected_book')
    # class Meta:
    #     model = Articles
    #     fields = ['title', 'full_name', 'desc', 'quote', 'biography', 'img']
    #     widgets = {
    #         'title': TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть назву (ім`я)'
    #         }),
    #         'full_name': TextInput(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть повну назву (ім`я)'
    #         }),
    #         'desc': Textarea(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть опис'
    #         }),
    #         'quote': Textarea(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть цитату'
    #         }),
    #         'biography': Textarea(attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Введіть біографію'
    #         })
    #     }


class UpdateHomePageForm(ModelForm):
    class Meta:
        model = HomePage
        fields = ['welcome_text', 'help_text']
        widgets = {
            'welcome_text': Textarea(attrs={
                'class': 'form-control',
            }),
            'help_text': Textarea(attrs={
                'class': 'form-control',
            })
        }


class CategoryForm(ModelForm):
    title = forms.CharField(label='Введіть назву', widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Введіть опис', widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Categories
        fields = ('title', 'description', 'img')
