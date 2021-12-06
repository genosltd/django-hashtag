# Modeled based on:
# https://docs.djangoproject.com/en/3.1/ref/contrib/contenttypes/#generic-relations

from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from django.db import models


class Hashtag(models.Model):
    hashtag = models.SlugField(unique=True)
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
        constraints = (
            models.UniqueConstraint(
                fields=('content_type_id', 'object_id'),
                name='unique_item'
            ),
        )

    hashtags = models.ManyToManyField(Hashtag, related_name='taggeditems',
                                      blank=True)

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
            instance.count = instance.taggeditems.count()
            instance.save()
        else:
            hashtags = list(model.objects.filter(id__in=pk_set))
            for hashtag in hashtags:
                hashtag.count = hashtag.taggeditems.count()
            model.objects.bulk_update(hashtags, fields=('count',))


class HasHashtags(models.Model):
    class Meta:
        abstract = True

    taggeditem = GenericRelation(TaggedItem)

    @property
    def hashtags(self):
        try:
            return self.taggeditem.first().hashtags

        except AttributeError:
            return self.taggeditem.create().hashtags
