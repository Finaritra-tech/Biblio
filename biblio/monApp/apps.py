from django.apps import AppConfig

class MonappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'monApp'

    def ready(self):
        import monApp.signals
