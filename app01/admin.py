from django.contrib import admin
from app01 import models


# Register your models here.
@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Articles)
class ArticlesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Tags)
class TagsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UpOrDowns)
class UpOrDownsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
