from django.core.management.base import BaseCommand
from app.models import Avis, Salle, Client, Utilisateur
import random

class Command(BaseCommand):
    help = 'Seeds the database with dummy reviews'

    def handle(self, *args, **options):
        salles = Salle.objects.all()
        if not salles.exists():
            self.stdout.write(self.style.ERROR('No salles found. Please create a salle first.'))
            return

        # Ensure we have a client to author the reviews
        client_user = Utilisateur.objects.filter(type_utilisateur='client').first()
        if not client_user:
            # Create a dummy client user if none exists
            email = 'testclient@example.com'
            client_user, created = Utilisateur.objects.get_or_create(
                email=email,
                defaults={
                    'full_name': 'Test Client',
                    'type_utilisateur': 'client',
                    'is_active': True,
                    'email_verified': True
                }
            )
            if created:
                client_user.set_password('password123')
                client_user.save()
        
        # Ensure the Client profile exists
        client, created = Client.objects.get_or_create(utilisateur=client_user)

        comments = [
            "Super salle, très propre !",
            "Les équipements sont un peu vieux mais l'ambiance est top.",
            "Le personnel est super accueillant, je recommande.",
            "Un peu cher pour la qualité du service.",
            "J'adore les cours de Yoga ici !",
            "Très bonne salle, propre et bien équipée.",
            "Excellent rapport qualité prix.",
            "L'instructeur de HIIT est super motivant."
        ]

        for salle in salles:
            self.stdout.write(f'Seeding reviews for {salle.nom}...')
            for _ in range(5):
                Avis.objects.create(
                    salle=salle,
                    client=client,
                    commentaire=random.choice(comments),
                    note_proprete=random.randint(3, 5),
                    note_equipement=random.randint(2, 5),
                    note_personnel=random.randint(4, 5),
                    note_rapport_qualite_prix=random.randint(3, 5)
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded reviews!'))
