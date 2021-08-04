from django.contrib import admin
from django_hashtag import admin as ht_admin

from . import models


@admin.register(models.TestModel)
class TestModelAdmin(ht_admin.TaggedItemBaseAdmin):
    pass
