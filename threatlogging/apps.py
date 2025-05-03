from django.apps import AppConfig

class ThreatloggingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'threatlogging'

    def ready(self):
        import threatlogging.log_signal