from django.contrib import admin

from app_books.models import *

admin.site.register(Books)
admin.site.register(Genres)
admin.site.register(Authors)
admin.site.register(Reviews)
admin.site.register(CommentReview)
