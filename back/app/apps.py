
from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    
    def ready(self):
        """
        Démarrer le scheduler au démarrage de Django
        """
        import os
        
        # ⚠️ IMPORTANT : Éviter de lancer 2 fois en mode debug
        if os.environ.get('RUN_MAIN') != 'true':
            return
        
        from app.scheduler import start_scheduler
        start_scheduler()


