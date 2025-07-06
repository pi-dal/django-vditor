from django.test import TestCase
from django.urls import reverse

from vditor_app.forms import VditorForm
from vditor_app.models import VditorTest, ExampleModel


class VditorTestModelTest(TestCase):
    def test_create_vditor_test_model(self):
        VditorTest.objects.create(content="<p>test content</p>")
        self.assertEqual(VditorTest.objects.count(), 1)
        obj = VditorTest.objects.first()
        self.assertEqual(obj.content, "<p>test content</p>")


class ExampleModelTest(TestCase):
    def test_create_example_model(self):
        ExampleModel.objects.create(name="test name", content="<p>test content</p>")
        self.assertEqual(ExampleModel.objects.count(), 1)
        obj = ExampleModel.objects.first()
        self.assertEqual(obj.name, "test name")
        self.assertEqual(obj.content, "<p>test content</p>")


class VditorFormTest(TestCase):
    def test_valid_form(self):
        data = {"name": "test name", "content": "<p>test content</p>"}
        form = VditorForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        data = {"name": "test name", "content": "<p>test content</p>"}
        form = VditorForm(data=data)
        self.assertTrue(form.is_valid())
        # VditorForm does not have a save method, so we don't call it.
        # This test only checks form validation.
        # If you want to test saving, it should be done in the view test.


class VditorTestViewTest(TestCase):
    def test_get_request(self):
        response = self.client.get(reverse("vditor_form"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")
        self.assertIsInstance(response.context["form"], VditorForm)

    def test_post_request_valid(self):
        data = {"name": "test name", "content": "<p>new content</p>"}
        response = self.client.post(reverse("vditor_form"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("vditor_form"))
        self.assertEqual(VditorTest.objects.count(), 1)
        self.assertEqual(VditorTest.objects.first().content, "<p>new content</p>")

    def test_post_request_invalid(self):
        # Assuming content is required
        data = {"name": "test name", "content": ""}
        response = self.client.post(reverse("vditor_form"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "form.html")
        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(VditorTest.objects.count(), 0)
