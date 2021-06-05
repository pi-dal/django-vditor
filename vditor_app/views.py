from __future__ import absolute_import

from django.urls import reverse
from django.views import generic

from . import forms


class VditorFormView(generic.FormView):
    form_class = forms.VditorForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("vditor_form")

vditor_form_view = VditorFormView.as_view()