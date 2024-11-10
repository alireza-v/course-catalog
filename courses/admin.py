from django.contrib import admin

from .models import Category, Comment, Course, Video


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("course", "descriptionSnippet", "score")

    def descriptionSnippet(self, obj):
        return obj.description[:50]


@admin.register(Video)
class ViewAdmin(admin.ModelAdmin):
    list_display = ("title", "video_file")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
