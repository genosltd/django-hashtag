# Modeled based on:
# https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations

from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django.db import models, transaction


class Hashtag(models.Model):
    class Meta:
        verbose_name = '#tag'

    hashtag = models.SlugField(unique=True, verbose_name='#tag')
    count = models.PositiveIntegerField(editable=False, default=0)

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
                fields=('content_type_id', 'object_id'),
                name='unique_item'
            ),
        )

    hashtags = models.ManyToManyField(Hashtag, related_name='tagged_items',
                                      verbose_name='#tags')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f"{self.content_object} tagged"


@receiver(m2m_changed, sender=TaggedItem.hashtags.through)
def hashtags_changed(sender, instance, action, reverse, model, pk_set,
                     **kwargs):
    if action.startswith('post_'):
        if reverse:
            instance.count = instance.tagged_items.count()
            instance.save()
        else:
            hashtags = list(model.objects.filter(id__in=pk_set))
            for hashtag in hashtags:
                hashtag.count = hashtag.tagged_items.count()
            model.objects.bulk_update(hashtags, fields=('count',))


class TaggedItemModel(models.Model):
    class Meta:
        abstract = True

    hashtags = GenericRelation(TaggedItem)
