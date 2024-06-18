from django.apps import AppConfig


class SongbirdConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'songbird'

    def ready(self):
        import songbird.startup
        import songbird.signals