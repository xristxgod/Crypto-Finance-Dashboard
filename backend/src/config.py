from __future__ import absolute_import

try:
    import settings as global_settings
except ModuleNotFoundError:
    import src.settings as global_settings

settings = global_settings.Settings()
