from django.apps import AppConfig


class ModuleTransfersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_transfers'

    def ready(self):
        import module_transfers.signals
