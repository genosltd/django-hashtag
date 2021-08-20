from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib import admin

from django_hashtag.admin import HasHashtagsAdmin

from test_app.models import TestModel
from test_app.admin import TestModelAdmin


class HasHashtagsAdminCase(TestCase):
    def test_get_inlines(self):
        test_model_admin = TestModelAdmin(TestModel, admin.site)
        request_factory = RequestFactory()
        request = request_factory.get(reverse('admin:test_app_testmodel_add'))

        inlines = test_model_admin.get_inlines(request)
        self.assertEqual(inlines, HasHashtagsAdmin.inlines)

    def test_get_inlines_with_override(self):
        TestModelAdmin.inlines = tuple()
        test_model_admin = TestModelAdmin(TestModel, admin.site)
        request_factory = RequestFactory()
        request = request_factory.get(reverse('admin:test_app_testmodel_add'))

        inlines = test_model_admin.get_inlines(request)
        self.assertEqual(inlines, HasHashtagsAdmin.inlines)
