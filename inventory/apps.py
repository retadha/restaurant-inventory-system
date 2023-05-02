from django.apps import AppConfig
from django.dispatch import receiver
from django.db.models.signals import post_save


class InventoriConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
