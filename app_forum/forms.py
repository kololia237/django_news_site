from functools import reduce

from django import forms
from django.forms import TextInput, Textarea, ModelForm

from app_forum.models import *
from app_forum.settings import *


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введіть назву'
            }),
            'description': Textarea(attrs={
                'class': 'form-control'
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 100px',
            })
        }

    def clean_body(self):
        body = self.cleaned_data["body"]

        if FORUM_FILTER_PROFANE_WORDS:
            profane_words = ProfaneWord.objects.all()
            bad_words = [w for w in profane_words if w.word in body.lower()]

            if bad_words:
                raise forms.ValidationError("Такі слова як '%s' заборонені." % (
                    reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))

        return body


# class ReplyForCommentForm(ModelForm):
#     class Meta:
#         model = ReplyForComment
#         fields = ['text']
#         widgets = {
#             'text': TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Введіть text'
#             })
#         }
#
#     def clean_body(self):
#         body = self.cleaned_data["text"]
#
#         if FORUM_FILTER_PROFANE_WORDS:
#             profane_words = ProfaneWord.objects.all()
#             bad_words = [w for w in profane_words if w.word in body.lower()]
#
#             if bad_words:
#                 raise forms.ValidationError("Такі слова як '%s' заборонені." % (
#                     reduce(lambda x, y: "%s,%s" % (x, y), bad_words)))
#
#         return body
