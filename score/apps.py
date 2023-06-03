from django.apps import AppConfig


class ScoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'score'
    
    def ready(self):
        from score import signals
