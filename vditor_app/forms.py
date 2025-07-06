from __future__ import absolute_import

from django import forms
from django.utils.translation import gettext_lazy as _

from vditor.fields import VditorTextFormField


class VditorForm(forms.Form):
    name = forms.CharField(label=_("Name"))
    content = VditorTextFormField(label=_("Content"))
