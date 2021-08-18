from django.db import models
from django_hashtag.models import HasHashtags


class TestModel(HasHashtags):
    test_field = models.CharField(max_length=100)

    def __str__(self):
        return str(self.test_field)
