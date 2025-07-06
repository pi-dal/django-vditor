from django.contrib import admin
from django.db import models

# Register your models here.
from . import models as demo_models
from vditor.widgets import VditorWidget


class ExampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": VditorWidget}}


admin.site.register(demo_models.ExampleModel, ExampleModelAdmin)
