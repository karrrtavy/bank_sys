from django.apps import AppConfig


class ModuleHoldingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'module_holding'
    
    def ready(self):
        import module_holding.signals