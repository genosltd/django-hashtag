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
        inlines = super().get_inlines(request, obj=obj)

        missing = frozenset(HasHashtagsAdmin.inlines) - frozenset(inlines)
        if missing:
            inlines = list(inlines)
            inlines.extend(missing)
            inlines = tuple(inlines)

        return inlines
