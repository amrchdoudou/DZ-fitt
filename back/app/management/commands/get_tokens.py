from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from app.models import Salle

class Command(BaseCommand):
    help = 'Affiche les tokens de tous les gérants'

    def handle(self, *args, **kwargs):
        print("\n" + "="*60)
        print("📋 LISTE DES TOKENS")
        print("="*60 + "\n")
        
        for salle in Salle.objects.all():
            token, _ = Token.objects.get_or_create(user=salle.gerant.utilisateur)
            
            print(f"Salle ID: {salle.id}")
            print(f"Nom: {salle.nom}")
            print(f"Gérant: {salle.gerant.utilisateur.full_name}")
            print(f"Email: {salle.gerant.utilisateur.email}")
            print(f"🔑 TOKEN: {token.key}")
            print("-"*60 + "\n")
            