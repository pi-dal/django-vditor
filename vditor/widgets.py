import json
import logging
from functools import lru_cache
from typing import Any, Dict, Optional

from django import forms
from django.core.cache import cache
from django.forms.utils import flatatt
from django.forms.widgets import get_default_renderer
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe

from .configs import VditorConfig

logger = logging.getLogger(__name__)

# Cache timeout for configurations (5 minutes)
CONFIG_CACHE_TIMEOUT = 300


class VditorWidget(forms.Textarea):
    def __init__(self, config_name: str = "default", *args: Any, **kwargs: Any) -> None:
        super(VditorWidget, self).__init__(*args, **kwargs)
        self.config_name = config_name
        try:
            self.config: VditorConfig = self._get_cached_config(config_name)
            logger.debug(f"Initialized VditorWidget with config '{config_name}'")
        except Exception as e:
            logger.error(f"Failed to initialize VditorConfig '{config_name}': {e}")
            # Fall back to default config
            self.config = self._get_cached_config("default")

    @lru_cache(maxsize=32)
    def _get_cached_config(self, config_name: str) -> VditorConfig:
        """Get configuration with caching to improve performance.

        Args:
            config_name: Name of configuration to load

        Returns:
            VditorConfig instance
        """
        cache_key = f"vditor_config_{config_name}"
        config_dict = cache.get(cache_key)

        if config_dict is None:
            # Load config and cache it
            config = VditorConfig(config_name)
            config_dict = dict(config)
            cache.set(cache_key, config_dict, CONFIG_CACHE_TIMEOUT)
            logger.debug(f"Cached configuration '{config_name}'")
        else:
            # Create config from cached dict
            config = VditorConfig.__new__(VditorConfig)
            config.update(config_dict)
            logger.debug(f"Using cached configuration '{config_name}'")

        return config

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

    @lru_cache(maxsize=1)
    def _get_media(self) -> forms.Media:
        """Get media files with caching for better performance."""
        return forms.Media(
            css={"all": ("dist/index.min.css",)},  # Use minified version in production
            js=("dist/index.min.js",),  # Use minified version in production
        )

    media = property(_get_media)
