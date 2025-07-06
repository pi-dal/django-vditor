from __future__ import absolute_import

from django.urls import reverse
from django.views import generic

from . import forms
from .models import VditorTest


class VditorFormView(generic.FormView):
    form_class = forms.VditorForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse("vditor_form")

    def form_valid(self, form):
        VditorTest.objects.create(
            name=form.cleaned_data["name"], content=form.cleaned_data["content"]
        )
        return super().form_valid(form)


vditor_form_view = VditorFormView.as_view()
