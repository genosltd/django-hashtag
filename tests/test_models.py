from django.test import TestCase

from django.contrib.contenttypes.models import ContentType
from django_hashtag import models

from test_app.models import TestModel


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
        user_type = ContentType.objects.get(app_label='test_app', model='testmodel')
        guido = user_type.model_class().objects.create(test_field='Guido')
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

    @classmethod
    def setUpTestData(cls):
        user_type = ContentType.objects.get(app_label='test_app', model='testmodel')
        guido = user_type.model_class().objects.create(test_field='Guido')
        dev = user_type.model_class().objects.create(test_field='dev')

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

        python.taggeditems.add(self.tagged_guido)
        python.refresh_from_db()

        self.assertEqual(python.count, 1)

        python.taggeditems.add(self.tagged_dev)
        python.refresh_from_db()

        self.assertEqual(python.count, 2)


class TaggedItemBaseTestCase(TestCase):
    def test_hashtags(self):
        a_model = TestModel.objects.create(test_field='test')
        self.assertQuerysetEqual(a_model.hashtags.all(), [])

        python = models.Hashtag.objects.create(hashtag='python')
        a_model.hashtags.add(python)
        self.assertQuerysetEqual(a_model.hashtags.all(), map(repr, (python,)))

        a_model.hashtags.remove(python)
        self.assertQuerysetEqual(a_model.hashtags.all(), [])
