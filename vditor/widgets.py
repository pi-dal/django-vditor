import json
import logging
from typing import Any, Dict, Optional

from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import get_default_renderer
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

from .configs import VditorConfig

logger = logging.getLogger(__name__)


class VditorWidget(forms.Textarea):
    def __init__(self, config_name: str = "default", *args: Any, **kwargs: Any) -> None:
        super(VditorWidget, self).__init__(*args, **kwargs)
        try:
            self.config: VditorConfig = VditorConfig(config_name)
            logger.debug(f"Initialized VditorWidget with config '{config_name}'")
        except Exception as e:
            logger.error(f"Failed to initialize VditorConfig '{config_name}': {e}")
            # Fall back to default config
            self.config = VditorConfig("default")

    def render(
        self,
        name: str,
        value: Any,
        attrs: Optional[Dict[str, Any]] = None,
        renderer: Any = None,
    ) -> str:
        if renderer is None:
            renderer = get_default_renderer()
        if value is None:
            value = ""
        final_attrs: Dict[str, Any] = self.build_attrs(self.attrs, attrs, name=name)

        # Ensure the id is present in final_attrs
        _id: Optional[str] = final_attrs.get("id")
        if not _id:
            _id = "id_" + name.replace(
                "-", "_"
            )  # Generate a predictable ID if not present
            final_attrs["id"] = _id

        context: Dict[str, Any] = {
            "final_attrs": flatatt(final_attrs),
            "value": force_str(value),
            "id": _id,
            "config": json.dumps(self.config),
        }

        try:
            rendered_html = renderer.render("widget.html", context)
            return mark_safe(rendered_html)
        except Exception as e:
            logger.error(f"Failed to render VditorWidget template: {e}")
            # Fallback to basic textarea
            return mark_safe(
                f'<textarea name="{name}" id="{_id}">{force_str(value)}</textarea>'
            )

    def build_attrs(
        self,
        base_attrs: Dict[str, Any],
        extra_attrs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        attrs: Dict[str, Any] = dict(base_attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def _get_media(self) -> forms.Media:
        return forms.Media(
            css={
                "all": (
                    "dist/index.css",
                    "dist/index.min.css",  # Add minified version
                )
            },
            js=(
                "dist/index.js",
                "dist/index.min.js",  # Add minified version
            ),
        )

    media = property(_get_media)
