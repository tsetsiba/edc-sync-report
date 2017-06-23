import os

from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style
from django.conf import settings

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'edc_sync_report'
    verbose_name = 'Data Synchronization'
    
    reports = os.path.join(
        settings.MEDIA, "transactions", "report")
