from django.apps import AppConfig


class TeacherhomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teacherhome'

    def ready(self):
        import teacherhome.signals
