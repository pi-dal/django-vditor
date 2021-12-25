<h1 align="center">django-vditor</h1>
<p align="center">
<img src="https://cdn.jsdelivr.net/gh/pi-dal/figure-bed@master/3A0F231C-4FF4-4041-A571-2CAA20CA5030.png" width="450" align="middle"></img>
</p>
<p align="center">
<strong>django-vditor</strong> is Markdown Editor plugin application for <a href="https://github.com/django/django">django</a> base on <a href="https://github.com/Vanessa219/vditor">vditor</a>.
<br>
<strong>django-vditor</strong> was inspired by great <a href="https://github.com/pylixm/django-mdeditor">django-mdeditor</a>.
<br><br>
<a title="python-version" target="_blank" href="https://github.com/pi-dal/django-vditor"><img alt="python-version" src="https://img.shields.io/badge/python-3.5+-purper.svg"></a>
<a title="django-version" target="_blank" href="https://pdm.fming.dev"><img alt="django-version" src="https://img.shields.io/badge/django-2.2+-green.svg"></a>
<a title="last-commit" target="_blank" href="https://github.com/pi-dal/django-vditor/commits/main"><img src="https://img.shields.io/github/last-commit/pi-dal/django-vditor?color=blue"></a> 
<a title="pdm-managed" target="_blank" href="https://github.com/frostming/pdm"><img src="https://img.shields.io/badge/pdm-managed-blueviolet"></a>
<br>
<a title="Codacy-Badge" target="_blank" href="https://www.codacy.com/gh/pi-dal/django-vditor/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pi-dal/django-vditor&amp;utm_campaign=Badge_Grade"><img src="https://img.shields.io/codacy/grade/d23000f233344a9891189a816b58f9b1"></a>
<a title="Codacy-Coveralls-Badge" target="_blank" href="https://www.codacy.com/gh/pi-dal/django-vditor/dashboard?utm_source=github.com&utm_medium=referral&utm_content=pi-dal/django-vditor&utm_campaign=Badge_Coverage"><img src="https://img.shields.io/codacy/coverage/d23000f233344a9891189a816b58f9b1"></a>
<a title="pypi" target="_blank" href="https://pypi.org/manage/project/django-vditor/releases"><img src="https://img.shields.io/pypi/v/django-vditor"></a><br>
<a title="license" target="_blank" href="https://github.com/pi-dal/django-vditor/blob/main/LICENSE"><img src="https://img.shields.io/github/license/pi-dal/django-vditor"/></a>
<br>
<a title="GitHub-Watchers" target="_blank" href="https://github.com/pi-dal/django-vditor/watchers"><img src="https://img.shields.io/github/watchers/pi-dal/django-vditor.svg?label=Watchers&style=social"></a>  
<a title="GitHub-Stars" target="_blank" href="https://github.com/pi-dal/django-vditor/stargazers"><img src="https://img.shields.io/github/stars/pi-dal/django-vditor.svg?label=Stars&style=social"></a>  
<a title="GitHub-Forks" target="_blank" href="https://github.com/pi-dal/django-vditor/network/members"><img src="https://img.shields.io/github/forks/pi-dal/django-vditor.svg?label=Forks&style=social"></a>  
<a title="Author-GitHub-Followers" target="_blank" href="https://github.com/pi-dal"><img src="https://img.shields.io/github/followers/pi-dal.svg?label=Followers&style=social"></a>
</p>

## Features

- Almost Vditor features
  - Support three editing modes: what you see is what you get (wysiwyg),    instant rendering (ir), split screen preview (sv)
  - Support outline, mathematical formulas, brain maps, charts, flowcharts, Gantt charts, timing charts, staff, multimedia, voice reading, title anchors, code highlighting and copying, graphviz rendering
  - Built-in security filtering, export, task list, multi-platform preview, multi-theme switching, copy to WeChat official account/Zhuhu function
  - Implement CommonMark and GFM specifications, format Markdown and view syntax tree, and support 10+ configurations
  - The toolbar contains 36+ operations. In addition to supporting extensions, you can customize the shortcut keys, prompts, prompt locations, icons, click events, class names, and sub-toolbars in each item.
  - You can use drag and drop, clipboard to paste upload, display real-time upload progress, and support CORS cross-domain upload
  - Pasted HTML is automatically converted to Markdown. If the pasted includes external link pictures, it can be uploaded to the server through the designated interface
  - Support main window size drag and drop, character count
  - Multi-theme support, built-in three sets of black and white themes
  - Multi-language support, built-in Chinese, English, and Korean text localization
  - Support mainstream browsers, friendly to mobile
- The VditorTextField field is provided for the model and can be displayed directly in the django admin.
- The VditorTextFormField is provided for the Form and ModelForm.
- The VditorWidget is provided for the Admin custom widget.

## Quick start

- Installation.

```bash
    # pip
    pip install django-vditor
    # pipenv
    pipenv install django-vditor
    # poetry
    poetry add django-vditor
    # pdm
    pdm add django-vditor
```

- Add `vditor` to your INSTALLED_APPS setting like this:

```python
    INSTALLED_APPS = [
        ...
        'vditor',
    ]
```

- add frame settings for django3.0+ like this：

```python
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

- Add 'media' url to your settings like this:

```python
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/media/'

```

- Add url to your urls like this:

```python
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
...

urlpatterns = [
    ...
    path('vditor/', include('vditor.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

- Write your models like this:

```python
from django.db import models
from vditor.fields import VditorTextField

class ExampleModel(models.Model):
    name = models.CharField(max_length=10)
    content = VditorTextField()
```

- Register your model in `admin.py`
- Run `python manage.py makemigrations` and `python manage.py migrate` to create your models.
- Login Admin ,you can see a markdown editor text field like this:

![django-vditor](https://github.com/pi-dal/figure-bed/blob/master/django-vditor.gif?raw=true)

## Usage

### Edit fields in the model using Markdown

Using Markdown to edit the fields in the model, we simply replace the `TextField` of the model with` VditorTextField`.

```python
from django.db import models
from vditor.fields import VditorTextField

class ExampleModel(models.Model):
    name = models.CharField(max_length = 10)
    content = VditorTextField()
```

Admin in the background, will automatically display markdown edit rich text.

Used in front-end template, you can use like this:

```html
{% load static %}
<! DOCTYPE html>
<html lang = "en">
    <head>
        <meta http-equiv = "Content-Type" content = "text/html; charset = utf-8" />
    </head>
    <body>
        <form method = "post" action = "./">
            {% csrf_token %}
            {{ form.media }}
            <ul style="display: flex">
                {{ form.as_p }}
            </ul>
            <p> <input type = "submit" value = "post"> </p>
        </form>
    </body>
</html>

```

### Edit fields in the Form using markdown

Use markdown to edit fields in the Form, use `VditorTextFormField` instead of` forms.CharField`, as follows:

```python
from vditor.fields import VditorTextFormField

class VditorForm(forms.Form):
    name = forms.CharField()
    content = VditorTextFormField()
```

`ModelForm` can automatically convert the corresponding model field to the form field, which can be used normally:

```python
class VditorModleForm(forms.ModelForm):

    class Meta:
        model = ExampleModel
        fields = '__all__'
```

### Use the markdown widget in admin

Use the markdown widget in admin like as :

```python
from django.contrib import admin
from django.db import models

# Register your models here.
from. import models as demo_models
from vditor.widgets import VditorWidget


class ExampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': VditorWidget}
    }


admin.site.register(demo_models.ExampleModel, ExampleModelAdmin)
```

### Customize the toolbar

Add the following configuration to `settings`:

```python
VDITOR_CONFIGS = { # remember to write "' '"
  'default':{
      "width": "%90", # use numbers or percentages
      "height": 360, # use numbers
      "preview_theme": "light", # can fill in dark, light, wechat
      "typewriterMode": "True", # whether to enable typewriter mode
      "mode": "ir", # optional modes: sv, ir, wysiwyg
      "debugger": "false", # whether to show log
      "value": "", # editor initialization value
      "theme": "classic", # can fill in classic, dark
      "icon": "ant", # canfill in ant, material
      "outline": "false", # show outline
  }
}
```

## Reference

- [django-mdeditor](https://github.com/pylixm/django-mdeditor)