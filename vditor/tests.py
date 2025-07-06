import json
import os
import uuid
from unittest.mock import patch, mock_open

from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ImproperlyConfigured

from vditor.widgets import VditorWidget
from vditor.configs import VditorConfig, get_default_config
from vditor.fields import VditorTextField, VditorTextFormField
from django import forms
from django.forms.widgets import get_default_renderer
from django.utils.safestring import mark_safe


@override_settings(MEDIA_ROOT="/tmp/media", MEDIA_URL="/media/")
class VditorImagesUploadViewTest(TestCase):

    def setUp(self):
        # Ensure MEDIA_ROOT exists before tests run
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

    def tearDown(self):
        # Clean up MEDIA_ROOT after tests run
        if os.path.exists(settings.MEDIA_ROOT):
            for root, dirs, files in os.walk(settings.MEDIA_ROOT, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(settings.MEDIA_ROOT)

    def test_image_upload_success(self):
        image_content = b"fake_image_content"
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )

        with patch(
            "uuid.uuid4", return_value=uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        ):
            response = self.client.post(
                reverse("uploads"), {"file[]": image_file}, format="multipart"
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], 0)
        self.assertEqual(response.json()["msg"], "Success!")
        expected_url = os.path.join(
            settings.MEDIA_URL, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa_test_image.png"
        )
        self.assertEqual(
            response.json()["data"]["succMap"]["test_image.png"], expected_url
        )

        # Verify file was saved
        expected_file_path = os.path.join(
            settings.MEDIA_ROOT, "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa_test_image.png"
        )
        self.assertTrue(os.path.exists(expected_file_path))
        with open(expected_file_path, "rb") as f:
            self.assertEqual(f.read(), image_content)

    def test_no_file_uploaded(self):
        response = self.client.post(reverse("uploads"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["code"], 1)
        self.assertEqual(response.json()["msg"], "No file uploaded.")

    def test_file_save_error(self):
        image_content = b"fake_image_content"
        image_file = SimpleUploadedFile(
            "test_image.png", image_content, content_type="image/png"
        )

        with patch("builtins.open", mock_open()) as mocked_file_open:
            mocked_file_open.side_effect = IOError("Disk full")
            response = self.client.post(
                reverse("uploads"), {"file[]": image_file}, format="multipart"
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()["code"], 1)
        self.assertEqual(response.json()["msg"], "Failed to save uploaded file.")


class VditorWidgetTest(TestCase):
    def test_init(self):
        widget = VditorWidget()
        self.assertIsInstance(widget.config, dict)
        self.assertEqual(widget.config["lang"], "en_US")  # Default language

        # Test with a custom config name
        with override_settings(VDITOR_CONFIGS={"custom": {"lang": "fr_FR"}}):
            widget_custom = VditorWidget(config_name="custom")
            self.assertIsInstance(widget_custom.config, dict)
            self.assertEqual(widget_custom.config["lang"], "fr_FR")

    def test_render_basic(self):
        widget = VditorWidget()
        name = "test_name"
        value = "test_value"
        rendered_html = widget.render(name, value)
        self.assertIn(f'name="{name}"', rendered_html)
        self.assertIn(f">{value}</textarea>", rendered_html)
        self.assertIn(f'id="id_{name}"', rendered_html)  # Check generated ID

    def test_render_with_attrs(self):
        widget = VditorWidget(attrs={"class": "my-class", "data-test": "test"})
        name = "test_name"
        value = "test_value"
        rendered_html = widget.render(name, value)
        self.assertIn('class="my-class"', rendered_html)
        self.assertIn('data-test="test"', rendered_html)

    def test_render_value_none(self):
        widget = VditorWidget()
        name = "test_name"
        value = None
        rendered_html = widget.render(name, value)
        self.assertIn(f"></textarea>", rendered_html)  # Empty textarea

    def test_render_id_from_attrs(self):
        widget = VditorWidget(attrs={"id": "my_custom_id"})
        name = "test_name"
        value = "test_value"
        rendered_html = widget.render(name, value)
        self.assertIn('id="my_custom_id"', rendered_html)
        self.assertNotIn('id="id_test_name"', rendered_html)

    @patch("vditor.widgets.get_default_renderer")
    def test_render_uses_renderer(self, mock_get_default_renderer):
        mock_renderer = mock_get_default_renderer.return_value
        mock_renderer.render.return_value = "mocked_html"

        widget = VditorWidget()
        name = "test_name"
        value = "test_value"
        rendered_html = widget.render(name, value)

        self.assertEqual(rendered_html, "mocked_html")
        mock_renderer.render.assert_called_once_with(
            "widget.html",
            {
                "final_attrs": ' cols="40" id="id_test_name" name="test_name" rows="10"',
                "value": "test_value",
                "id": "id_test_name",
                "config": json.dumps(VditorConfig()),
            },
        )

    def test_build_attrs(self):
        widget = VditorWidget()
        base_attrs = {"rows": 10}
        extra_attrs = {"cols": 80, "class": "editor"}
        result = widget.build_attrs(base_attrs, extra_attrs, name="content")
        self.assertEqual(
            result, {"rows": 10, "cols": 80, "class": "editor", "name": "content"}
        )

    def test_media_property(self):
        widget = VditorWidget()
        media = widget.media
        self.assertIsInstance(media, forms.Media)
        self.assertIn("dist/index.css", media._css["all"])
        self.assertIn("dist/index.min.css", media._css["all"])
        self.assertIn("dist/index.js", media._js)
        self.assertIn("dist/index.min.js", media._js)


class VditorConfigTest(TestCase):
    def test_get_default_config(self):
        config = get_default_config()
        self.assertIsInstance(config, dict)
        self.assertIn("width", config)
        self.assertEqual(config["width"], "100%")
        self.assertIn("lang", config)
        self.assertEqual(
            config["lang"], "zh_CN"
        )  # Default language in get_default_config

    def test_vditor_config_init_default(self):
        config = VditorConfig()
        self.assertIsInstance(config, dict)
        self.assertEqual(
            config["lang"], "en_US"
        )  # Default language set by set_language

    @override_settings(LANGUAGE_CODE="fr")
    def test_vditor_config_init_custom_language(self):
        config = VditorConfig()
        self.assertEqual(config["lang"], "fr_FR")

    @override_settings(
        VDITOR_CONFIGS={"my_custom_config": {"width": "50%", "mode": "sv"}}
    )
    def test_vditor_config_init_custom_config(self):
        config = VditorConfig(config_name="my_custom_config")
        self.assertEqual(config["width"], "50%")
        self.assertEqual(config["mode"], "sv")
        self.assertEqual(config["lang"], "en_US")  # Should still be default lang

    @override_settings(VDITOR_CONFIGS="not_a_dict")
    def test_vditor_config_improperly_configured_not_dict(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured, "VDITOR_CONFIGS setting must be a dictionary type."
        ):
            VditorConfig(config_name="default")

    @override_settings(VDITOR_CONFIGS={"other_config": {}})
    def test_vditor_config_improperly_configured_config_not_found(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "No configuration named ''non_existent'' found in your VDITOR_CONFIGS setting.",
        ):
            VditorConfig(config_name="non_existent")

    @override_settings(VDITOR_CONFIGS={"invalid_config": "not_a_dict"})
    def test_vditor_config_improperly_configured_config_value_not_dict(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            'VDITOR_CONFIGS["invalid_config"] setting must be a dictionary type.',
        ):
            VditorConfig(config_name="invalid_config")


class VditorFieldsTest(TestCase):
    def test_vditor_text_field_formfield(self):
        field = VditorTextField()
        form_field = field.formfield()
        self.assertIsInstance(form_field, VditorTextFormField)

    def test_vditor_text_form_field_widget(self):
        form_field = VditorTextFormField()
        self.assertIsInstance(form_field.widget, VditorWidget)
