from django.db import models
from django_hashtag import models as ht_models


class AModel(ht_models.TaggedItemModel):
    a_field = models.CharField(max_length=100)
