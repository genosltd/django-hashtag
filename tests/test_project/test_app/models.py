from django.db import models
from django_hashtag import models as ht_models


class TestModel(ht_models.TaggedItemBase):
    test_field = models.CharField(max_length=100)
