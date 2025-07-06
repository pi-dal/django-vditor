from typing import Any, Dict, Type

from django.db import models
from django import forms
from .widgets import VditorWidget


class VditorTextField(models.TextField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.config_name: str = kwargs.pop("config_name", "default")
        super(VditorTextField, self).__init__(*args, **kwargs)

    @staticmethod
    def _get_form_class() -> Type["VditorTextFormField"]:
        return VditorTextFormField

    def formfield(self, **kwargs: Any) -> "VditorTextFormField":
        defaults: Dict[str, Any] = {
            "form_class": self._get_form_class(),
            "config_name": self.config_name,
        }
        defaults.update(kwargs)
        return super(VditorTextField, self).formfield(**defaults)


class VditorTextFormField(forms.fields.CharField):
    def __init__(self, config_name: str = "default", *arg: Any, **kwargs: Any) -> None:
        kwargs.update({"widget": VditorWidget(config_name=config_name)})
        super(VditorTextFormField, self).__init__(*arg, **kwargs)
