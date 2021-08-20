from django.contrib import admin
from django_hashtag.admin import HasHashtagsAdmin

from . import models


@admin.register(models.TestModel)
class TestModelAdmin(HasHashtagsAdmin):
    pass
