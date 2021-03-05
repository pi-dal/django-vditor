from django.db import models
from vditor.fields import VditorTextField


class ExampleModel(models.Model):
    name = models.CharField(max_length = 10)
    content = VditorTextField()

class VditorTest(models.Model):
    name = models.CharField(max_length = 10)
    content = VditorTextField()
