from django.contrib import admin

from app_forum.models import *


class ForumAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "forum", "creator", "created"]
    list_filter = ["forum", "creator"]


class CommentAdmin(admin.ModelAdmin):
    search_fields = ["creator"]
    list_display = ["topic", "creator", "created"]


class ReplyForCommentAdmin(admin.ModelAdmin):
    search_fields = ["text", "creator"]
    list_display = ["text", "comment", "creator", "created"]


class ProfaneWordAdmin(admin.ModelAdmin):
    pass


admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(ReplyForComment, ReplyForCommentAdmin)
admin.site.register(ProfaneWord, ProfaneWordAdmin)
