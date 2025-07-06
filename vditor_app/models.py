from django.db import models
from django.utils.translation import gettext_lazy as _
from vditor.fields import VditorTextField


class ExampleModel(models.Model):
    name = models.CharField(_("Name"), max_length=10)
    content = VditorTextField(_("Content"))


class VditorTest(models.Model):
    name = models.CharField(_("Name"), max_length=10)
    content = VditorTextField(_("Content"))
