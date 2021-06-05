from __future__ import absolute_import

from django import forms

from vditor.fields import VditorTextFormField


class VditorForm(forms.Form):
    name = forms.CharField()
    content = VditorTextFormField()