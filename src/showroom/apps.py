from django.apps import AppConfig


class ShowroomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.showroom'

    def ready(self):
        import src.showroom.signals
