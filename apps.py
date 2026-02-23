from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TrainingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training'
    label = 'training'
    verbose_name = _('Training & Skills')

    def ready(self):
        pass
