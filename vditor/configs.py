from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

#There are currently fewer options, more options will be added in the future
DEFAULT_CONFIG = {
    "width": "%90",
    "height": 360,
    "preview_theme": "light",
    "typewriterMode": "True",
    "mode": "ir",
    "debugger": "false",
    "value": "",
    "theme": "classic",
    "icon": "ant",
    "outline": "false",
}

if settings.LANGUAGE_CODE == "zh-Hans":
    DEFAULT_CONFIG["lang"] = "zh_CN"
elif settings.LANGUAGE_CODE == "ja-jp":
    DEFAULT_CONFIG["lang"] = "ja_JP"
elif settings.LANGUAGE_CODE == "ko-kr":
    DEFAULT_CONFIG["lang"] = "ko_KR"
else:
    DEFAULT_CONFIG["lang"] = "en_US"

class VditorConfig(dict):
    def __init__(self, config_name = "default"):
        self.update(DEFAULT_CONFIG)
        self.set_configs(config_name)

    def set_configs(self, config_name = "default"):
        configs = getattr(settings, "VDITOR_CONFIGS", None)
        if configs:
            if isinstance(configs, dict):
                if config_name in configs:
                    config = configs[config_name]
                    if not isinstance(config, dict):
                        raise ImproperlyConfigured('VDITOR_CONFIGS["%s"] \
                                        setting must be a dictionary type.' %config_name)
                    self.update(config)
                else:
                    raise ImproperlyConfigured("No configuration named '%s' \
                                    found in your VDITOR_CONFIGS setting." %config_name)
            else:
                raise ImproperlyConfigured('VDITOR_CONFIGS setting must be a\
                                dictionary type.')
