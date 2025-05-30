from django.apps import AppConfig


class ModuleAccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_account'

    def ready(self):
        import module_account.signals
