from django.apps import AppConfig


class IpoApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ipo_api'
    
    def ready(self):
        import ipo_api.signals
