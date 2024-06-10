from django.apps import AppConfig


class MessengConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messeng'

    def ready(self):
        import messeng.signals
