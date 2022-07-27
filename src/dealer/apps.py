from django.apps import AppConfig


class DealerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.dealer'

    def ready(self):
        import src.dealer.signals
