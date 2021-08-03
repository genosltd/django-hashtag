from django.test import TestCase

from django.contrib.contenttypes.models import ContentType
from django_hashtag import models


class HashtagTestCase(TestCase):
    def test__str__(self):
        hashtag = models.Hashtag.objects.create(hashtag='tag')
        self.assertEqual(str(hashtag), '#tag')

    def test_save_tag_without_hash(self):
        hashtag = models.Hashtag(hashtag='tag')
        hashtag.save()
        self.assertEqual(str(hashtag.hashtag), '#tag')

    def test_save_tag_with_hash(self):
        hashtag = models.Hashtag(hashtag='#tag')
        hashtag.save()
        self.assertEqual(str(hashtag.hashtag), '#tag')


class TaggedItemTestCase(TestCase):
    def test__str__(self):
        user_type = ContentType.objects.get(app_label='auth', model='user')
        guido = user_type.model_class().objects.create(username='Guido')
        tagged_guido = models.TaggedItem.objects.create(content_type=user_type,
                                                        object_id=guido.id)

        self.assertEqual(str(tagged_guido), 'Guido tagged')


class HashtagsChangedTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_type = ContentType.objects.get(app_label='auth', model='user')
        guido = user_type.model_class().objects.create(username='Guido')
        dev = user_type.model_class().objects.create(username='dev')

        cls.tagged_guido = models.TaggedItem.objects.create(
            content_type=user_type,
            object_id=guido.id
        )
        cls.tagged_dev = models.TaggedItem.objects.create(
            content_type=user_type,
            object_id=dev.id
        )
        cls.python = models.Hashtag.objects.create(hashtag='python')

    def test_forward(self):
        python = self.python

        self.tagged_guido.hashtags.add(python)
        python.refresh_from_db()

        self.assertEqual(python.count, 1)

        self.tagged_dev.hashtags.add(python)
        python.refresh_from_db()

        self.assertEqual(python.count, 2)

    def test_reverse(self):
        python = self.python

        python.tagged_items.add(self.tagged_guido)
        python.refresh_from_db()

        self.assertEqual(python.count, 1)

        python.tagged_items.add(self.tagged_dev)
        python.refresh_from_db()

        self.assertEqual(python.count, 2)
