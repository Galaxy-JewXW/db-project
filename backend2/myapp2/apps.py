from django.apps import AppConfig


class Myapp2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp2'

    def ready(self):
        import myapp2.signals
