from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib import admin

from . import models


@admin.register(models.Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    search_fields = ('hashtag',)
    list_display = ('hashtag', 'count')
    ordering = ('-count', 'hashtag')


class TaggedItemInline(GenericStackedInline):
    model = models.TaggedItem
    autocomplete_fields = ('hashtags',)
    extra = 0
    max_num = 1
    min_num = 1
    template = 'tagged-item-inline.html'


class HasHashtagsAdmin(admin.ModelAdmin):
    inlines = (TaggedItemInline,)

    def get_inlines(self, request, obj=None):
        inlines = list(super().get_inlines(request, obj=obj))

        for inline in reversed(HasHashtagsAdmin.inlines):
            if inline not in inlines:
                inlines.insert(0, inline)

        return tuple(inlines)
