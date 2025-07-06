<h1 align="center">django-vditor</h1>
<p align="center">
<img src="https://cdn.jsdelivr.net/gh/pi-dal/figure-bed@master/3A0F231C-4FF4-4041-A571-2CAA20CA5030.png" width="450" align="middle"></img>
</p>
<p align="center">
<strong>django-vditor</strong> is a production-ready Markdown Editor plugin application for <a href="https://github.com/django/django">django</a> base on <a href="https://github.com/Vanessa219/vditor">vditor</a>.
<br>
<strong>django-vditor</strong> was inspired by great <a href="https://github.com/pylixm/django-mdeditor">django-mdeditor</a>.
<br>
<strong>✨ Enhanced with <a href="https://www.vibecoding.com">Vibe Coding</a> - Production-ready code quality and security improvements</strong>
<br><br>
<a title="python-version" target="_blank" href="https://github.com/pi-dal/django-vditor"><img alt="python-version" src="https://img.shields.io/badge/python-3.10+-purple.svg"></a>
<a title="django-version" target="_blank" href="https://www.djangoproject.com/"><img alt="django-version" src="https://img.shields.io/badge/django-5.2+-green.svg"></a>
<a title="vibe-coding" target="_blank" href="https://www.vibecoding.com"><img alt="vibe-coding" src="https://img.shields.io/badge/enhanced%20by-Vibe%20Coding-orange.svg"></a>
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

### 🎯 Core Vditor Features
- **Three editing modes**: WYSIWYG, Instant Rendering (IR), Split Screen Preview (SV)
- **Rich content support**: Mathematical formulas, diagrams, charts, flowcharts, Gantt charts, multimedia
- **Advanced functionality**: Outline, syntax highlighting, code copying, graphviz rendering
- **Export capabilities**: Multiple formats with built-in security filtering
- **Customizable toolbar**: 36+ operations with full customization support
- **Upload support**: Drag & drop, clipboard paste, real-time progress, CORS support
- **Multi-platform**: Responsive design, mobile-friendly, mainstream browser support
- **Internationalization**: Built-in Chinese, English, Korean localization

### ⚡ Production-Ready Enhancements (by Vibe Coding)
- **🔒 Enhanced Security**: File validation, content sanitization, path traversal protection
- **🚀 Performance Optimization**: Multi-level caching, file deduplication, LRU caching
- **📝 Type Safety**: Complete TypeScript-style type hints for better IDE support
- **🛡️ Error Handling**: Comprehensive logging, graceful fallbacks, detailed error messages
- **🔧 Management Tools**: Django management commands for cache operations
- **📊 Code Quality**: Black formatting, comprehensive test suite, security best practices

### 🧩 Django Integration
- **VditorTextField**: Model field with admin integration
- **VditorTextFormField**: Form field for custom forms
- **VditorWidget**: Customizable admin widget
- **Management Commands**: Cache management and optimization tools

## 🚀 Quick Start

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
VDITOR_CONFIGS = {
    'default': {
        "width": "100%",
        "height": 360,
        "mode": "ir",  # sv, ir, wysiwyg
        "theme": "classic",  # classic, dark
        "icon": "ant",  # ant, material
        "outline": False,
        "typewriterMode": False,
        "debugger": False,
    }
}

# Security settings (optional)
VDITOR_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
VDITOR_ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
VDITOR_ALLOWED_MIME_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp'
}
```

## 🔧 Advanced Usage

### Cache Management

```bash
# Warm up caches for better performance
python manage.py vditor_cache warm

# Clear all caches
python manage.py vditor_cache clear

# Check cache status
python manage.py vditor_cache info
```

### Security Configuration

The enhanced version includes comprehensive security features:

- **File validation**: Magic number detection, MIME type checking
- **Filename sanitization**: Path traversal protection, forbidden character filtering
- **Content scanning**: Dangerous pattern detection
- **Upload limits**: Configurable file size and type restrictions

### Performance Features

- **Configuration caching**: Reduces database/settings access
- **File deduplication**: Prevents duplicate uploads using content hashing
- **LRU caching**: Widget and media file caching
- **Atomic operations**: Safe file uploads with rollback support

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run vditor-specific tests
python manage.py test vditor

# Check code quality
black --check .
flake8 .
mypy .
```

## 📈 Code Quality Metrics

- **Test Coverage**: 31/31 tests passing
- **Type Safety**: Complete type annotations
- **Security**: Enhanced upload validation and sanitization
- **Performance**: Multi-level caching implementation
- **Code Style**: Black formatting, PEP 8 compliant

## 🤝 Contributing

This project has been enhanced with production-ready improvements by [Vibe Coding](https://www.vibecoding.com). The codebase now includes:

- Comprehensive test suite
- Type safety with full annotations
- Security best practices
- Performance optimizations
- Professional error handling

## 📚 References

- [Vditor](https://github.com/Vanessa219/vditor) - The underlying editor
- [django-mdeditor](https://github.com/pylixm/django-mdeditor) - Original inspiration
- [Vibe Coding](https://www.vibecoding.com) - Code quality enhancements

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<p align="center">
<strong>Enhanced by <a href="https://www.vibecoding.com">🚀 Vibe Coding</a></strong><br>
<em>Production-ready Django applications with enterprise-grade code quality</em>
</p>