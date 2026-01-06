from django.core.management.base import BaseCommand
from app.models import Salle, Gerant, Utilisateur

class Command(BaseCommand):
    help = 'Vérifie les salles et gérants dans la base'

    def handle(self, *args, **kwargs):
        print("\n" + "="*60)
        print("📊 ÉTAT DE LA BASE DE DONNÉES")
        print("="*60 + "\n")
        
        # Compter les utilisateurs
        total_users = Utilisateur.objects.count()
        gerants_count = Gerant.objects.count()
        salles_count = Salle.objects.count()
        
        print(f"👥 Total utilisateurs: {total_users}")
        print(f"🏋️ Gérants: {gerants_count}")
        print(f"🏢 Salles: {salles_count}")
        print("\n" + "-"*60 + "\n")
        
        # Lister les gérants
        if gerants_count > 0:
            print("📋 LISTE DES GÉRANTS:")
            for gerant in Gerant.objects.all():
                print(f"\n  Gérant ID: {gerant.id}")
                print(f"  Nom: {gerant.utilisateur.full_name}")
                print(f"  Email: {gerant.utilisateur.email}")
                print(f"  Statut: {gerant.statut_approbation}")
                print(f"  Compte actif: {gerant.utilisateur.is_active}")
                print(f"  Nombre de salles: {gerant.salles.count()}")
        else:
            print("❌ Aucun gérant trouvé")
        
        print("\n" + "-"*60 + "\n")
        
        # Lister les salles
        if salles_count > 0:
            print("🏢 LISTE DES SALLES:")
            for salle in Salle.objects.all():
                print(f"\n  Salle ID: {salle.id}")
                print(f"  Nom: {salle.nom}")
                print(f"  Gérant: {salle.gerant.utilisateur.full_name}")
        else:
            print("❌ Aucune salle trouvée")
            print("\n💡 Pour créer une salle, tu dois:")
            print("   1. Avoir un compte gérant approuvé")
            print("   2. Te connecter avec ce compte")
            print("   3. Créer une salle via l'API POST /api/my-salles/")
        
        print("\n" + "="*60 + "\n")