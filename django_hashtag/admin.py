from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib import admin

from . import models


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    search_fields = ('hashtag',)


class TaggedItemInline(GenericStackedInline):
    model = models.TaggedItem
    autocomplete_fields = ('hashtags',)
    extra = 0
    max_num = 1
    min_num = 1


class TaggedItemModelAdmin(admin.ModelAdmin):
    inlines = (TaggedItemInline,)
