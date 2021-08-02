# Modeled based on:
# https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations

from django.contrib.contenttypes.fields import GenericForeignKey, \
                                                GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models


class Hashtag(models.Model):
    class Meta:
        verbose_name = '#tag'

    hashtag = models.SlugField(unique=True, verbose_name='#tag')

    def save(self, *args, **kwargs):
        hashtag = self.hashtag
        if not hashtag.startswith('#'):
            self.hashtag = '#' + hashtag

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.hashtag)


class TaggedItem(models.Model):
    class Meta:
        verbose_name = '#tag'
        constraints = (
            models.UniqueConstraint(
                fields=('hashtag_id', 'content_type_id', 'object_id'),
                name='unique_tag'
            ),
        )

    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE,
                                verbose_name='#tag')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.hashtag.hashtag}"

    # FIXME: not working correctly
    def validate_unique(self, exclude=None):
        tagged_items = TaggedItem.objects.filter(
            hashtag_id=self.hashtag_id,
            content_type_id=self.content_type_id,
            object_id=self.object_id
        )
        if tagged_items.count() > 0:
            raise ValidationError(f"Duplicate hashtag error: "
                                  f"'{self.hashtag}' can be used only once.")

        super().validate_unique(exclude=exclude)


class TaggedItemModel(models.Model):
    class Meta:
        abstract = True

    hashtags = GenericRelation(TaggedItem)
