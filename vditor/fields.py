from django.db import models
from django import forms
from .widgets import VditorWidget


class VditorTextField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop("config_name", "default")
        super(VditorTextField, self).__init__(*args, **kwargs)

    @staticmethod
    def _get_form_class():
        return VditorTextFormField

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self._get_form_class(),
            "config_name": self.config_name,
        }
        defaults.update(kwargs)
        return super(VditorTextField, self).formfield(**defaults)


class VditorTextFormField(forms.fields.CharField):
    def __init__(self, config_name="default", *arg, **kwargs):
        kwargs.update({"widget": VditorWidget(config_name=config_name)})
        super(VditorTextFormField, self).__init__(*arg, **kwargs)
