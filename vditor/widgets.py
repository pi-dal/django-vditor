from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import get_default_renderer
from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from .configs import VditorConfig

class VditorWidget(forms.Textarea):
    def __init__(self, config_name = 'default', *args, **kwargs):
        super(VditorWidget, self).__init__(*args, **kwargs)
        self.config = VditorConfig(config_name)

    def render(self, value, name, attrs=None, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ""
        final_attrs = self.build_attrs(self.attrs, attrs, name=name)
        
        return mark_safe(
            renderer.render(
                'widget.html',
                {
                    'final_attrs': flatatt(final_attrs),
                    'value': conditional_escape(force_text(value)),
                    'id': final_attrs['id'],
                    'config': self.config,
                }
                )
            )

    def build_attrs(self, base_attrs, extra_attrs=None, **kwargs):
        attrs = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def _get_media(self):
        return forms.Media(
            css={
                "all": ("dist/index.css",)
            },
            js=(
                "dist/index.min.js",
            ))
    media = property(_get_media)