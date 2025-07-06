import logging
from typing import Any, Dict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

logger = logging.getLogger(__name__)


def get_default_config() -> Dict[str, Any]:
    return {
        "width": "100%",
        "height": "auto",
        "minHeight": 360,
        "placeholder": "",
        "lang": "zh_CN",
        "mode": "ir",  # "sv", "ir", "wysiwyg"
        "value": "",
        "theme": "classic",  # "classic", "dark"
        "icon": "ant",  # "ant", "material"
        "typewriterMode": False,
        "debugger": False,
        "toolbar": [
            "emoji",
            "headings",
            "bold",
            "italic",
            "strike",
            "link",
            "|",
            "list",
            "ordered-list",
            "check",
            "outdent",
            "indent",
            "|",
            "quote",
            "line",
            "code",
            "inline-code",
            "insert-after",
            "insert-before",
            "|",
            "upload",
            "record",
            "table",
            "|",
            "undo",
            "redo",
            "|",
            "fullscreen",
            "edit-mode",
            "preview",
            "outline",
            "code-theme",
            "content-theme",
            "export",
            "|",
            "devtools",
            "info",
            "help",
            "|",
            "br",
        ],
        "counter": {
            "enable": False,
            "max": 200000,
            "type": "word",
        },
        "cache": {
            "enable": False,
            "id": None,
        },
        "preview": {
            "delay": 500,
            "maxWidth": 768,
            "mode": "both",
            "url": "",
            "hljs": {
                "enable": True,
                "lineNumber": False,
                "style": "github",
                "languages": [],
            },
            "markdown": {
                "autoSpace": True,
                "fixTermTypo": True,
                "footnotes": True,
                "linkToFootnotes": True,
                "paragraphBeginningSpace": True,
                "setext": True,
                "theme": "light",  # "dark", "light", "wechat"
            },
            "actions": [],
        },
        "upload": {
            "url": "",
            "max": 10 * 1024 * 1024,
            "token": None,
            "fieldName": "file[]",
            "extraData": {},
            "extraHeaders": {},
            "withCredentials": False,
            "file": None,
            "success": None,
            "error": None,
            "filename": None,
            "linkToImgUrl": "",
        },
        "hint": {
            "enable": True,
            "extend": [],
            "emoji": {
                "'+1'": "👍",
                "'-1'": "👎",
                "'laugh'": "😂",
                "'hooray'": "🎉",
                "'confused'": "😕",
                "'heart'": "❤️",
                "'rocket'": "🚀",
                "'eyes'": "👀",
            },
        },
        "resize": {
            "enable": False,
            "position": "bottom",
            "after": None,
        },
        "tab": "\t",
        "outline": {
            "enable": False,
            "position": "left",
        },
        "undoDelay": 200,
        "after": None,
        "blur": None,
        "focus": None,
        "esc": None,
        "ctrlEnter": None,
        "select": None,
        "input": None,
        "spin": False,
        "toolbarConfig": {
            "pin": False,
        },
        "keymap": {
            "mac": [],
            "win": [],
        },
        "type": "markdown",
        "className": "",
        "cSpell": "",
        "speech": {
            "enable": False,
            "lang": "zh_CN",
        },
        "fullscreen": {
            "index": 999,
        },
        "scroll": {
            "enable": False,
            "target": None,
        },
        "selectText": None,
        "themeMode": "auto",
    }


class VditorConfig(dict):
    def __init__(self, config_name: str = "default") -> None:
        # Try to load from cache first
        try:
            from .cache_utils import ConfigCache

            cached_config = ConfigCache.get_config(config_name)
            if cached_config:
                self.update(cached_config)
                logger.debug(f"Loaded config '{config_name}' from cache")
                return
        except ImportError:
            # Cache utils not available, proceed normally
            pass

        # Cache miss or not available - build config
        self.update(get_default_config())
        self.set_language()
        self.set_configs(config_name)

        # Cache the result
        try:
            from .cache_utils import ConfigCache

            ConfigCache.set_config(config_name, dict(self))
        except ImportError:
            pass

    def set_language(self) -> None:
        language_map: Dict[str, str] = {
            "zh-hans": "zh_CN",
            "ja": "ja_JP",
            "ko": "ko_KR",
            "en": "en_US",
            "fr": "fr_FR",
            "ru": "ru_RU",
            "de": "de_DE",
            "sv": "sv_SE",
            "pt-br": "pt_BR",
            "zh-tw": "zh_TW",
        }
        self["lang"] = language_map.get(settings.LANGUAGE_CODE, "en_US")

    def set_configs(self, config_name: str = "default") -> None:
        """Load and apply configuration from Django settings.

        Args:
            config_name: Name of the configuration to load

        Raises:
            ImproperlyConfigured: If configuration is invalid
        """
        configs: Any = getattr(settings, "VDITOR_CONFIGS", None)
        if configs:
            logger.debug(f"Loading Vditor configuration: {config_name}")

            if not isinstance(configs, dict):
                error_msg = "VDITOR_CONFIGS setting must be a dictionary type."
                logger.error(error_msg)
                raise ImproperlyConfigured(error_msg)

            if config_name in configs:
                config: Any = configs[config_name]
                if not isinstance(config, dict):
                    error_msg = f'VDITOR_CONFIGS["{config_name}"] setting must be a dictionary type.'
                    logger.error(error_msg)
                    raise ImproperlyConfigured(error_msg)

                logger.debug(
                    f"Applied configuration '{config_name}' with {len(config)} settings"
                )
                self.update(config)
            else:
                available_configs = list(configs.keys())
                error_msg = (
                    f"No configuration named '{config_name}' found in your VDITOR_CONFIGS setting. "
                    f"Available configurations: {available_configs}"
                )
                logger.error(error_msg)
                raise ImproperlyConfigured(error_msg)
        else:
            logger.debug(
                f"Using default configuration for '{config_name}' (no VDITOR_CONFIGS found)"
            )
