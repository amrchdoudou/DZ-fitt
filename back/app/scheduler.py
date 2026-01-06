from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def cleanup_unverified_users():
    """
    Fonction appelée par le scheduler pour nettoyer les comptes non vérifiés
    """
    try:
        from app.models import Utilisateur, VerificationCode
        
        limite = timezone.now() - timedelta(hours=24)
        
        users_to_delete = Utilisateur.objects.filter(
            email_verified=False,
            dateInscription__lt=limite
        )
        
        count = users_to_delete.count()
        
        if count > 0:
            emails = list(users_to_delete.values_list('email', flat=True))
            VerificationCode.objects.filter(email__in=emails).delete()
            users_to_delete.delete()
            
            logger.info(f"✅ {count} compte(s) non vérifié(s) supprimé(s)")
            for email in emails:
                logger.info(f"   - {email}")
        else:
            logger.info("⚠️ Aucun compte à supprimer")
            
    except Exception as e:
        logger.error(f"❌ Erreur lors du nettoyage : {str(e)}")


def start_scheduler():
    """
    Démarre le scheduler en arrière-plan
    """
    scheduler = BackgroundScheduler()
    
    # Exécuter toutes les heures
    scheduler.add_job(
        cleanup_unverified_users,
        'interval',
        hours=1,
        id='cleanup_unverified_users',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("🚀 Scheduler démarré - Nettoyage automatique activé")

