from django.contrib import admin
from .models import POST, Comment, Postlikes


@admin.register(POST)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "slug", "created_data", "update_data", "image", "title",)
    list_filter = ("user", "slug", "title","created_data", )
    search_fields = ("title", "user", "slug",)
    prepopulated_fields = {"slug":("title",)}
    raw_id_fields = ("user",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post","reply", "is_reply")
    raw_id_fields = ("user", "post", "reply")

admin.site.register(Postlikes)









