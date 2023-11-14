from django.apps import AppConfig


class BaseConfig(AppConfig):
    verbose_name = 'Магазин'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.store'
