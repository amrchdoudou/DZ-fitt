from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from app.models import Utilisateur, VerificationCode

class Command(BaseCommand):
    help = 'Supprime les utilisateurs non vérifiés après 24 heures'

    def handle(self, *args, **kwargs):
        # Date limite : 24h en arrière
        limite = timezone.now() - timedelta(hours=24)
        
        # Trouver les utilisateurs non vérifiés créés il y a plus de 24h
        users_to_delete = Utilisateur.objects.filter(
            email_verified=False,
            dateInscription__lt=limite
        )
        
        count = users_to_delete.count()
        
        if count > 0:
            # Supprimer les codes de vérification associés
            emails = users_to_delete.values_list('email', flat=True)
            VerificationCode.objects.filter(email__in=emails).delete()
            
            # Supprimer les utilisateurs
            users_to_delete.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ {count} utilisateur(s) non vérifié(s) supprimé(s)'
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ Aucun utilisateur à supprimer')
            )
