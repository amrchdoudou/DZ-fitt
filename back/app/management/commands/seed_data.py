# app/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from app.models import Equipement, Service


class Command(BaseCommand):
    help = 'Seed equipment and services data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('🌱 Starting data seeding...'))
        
        # ==========================================
        # EQUIPMENT
        # ==========================================
        equipment_list = [
            'Tapis de course',
            'Vélo elliptique',
            'Vélo stationnaire',
            'Haltères',
            'Bancs de musculation',
            'Machines de musculation',
            'Barres et disques',
            'Kettlebells',
            'TRX',
            'Sacs de frappe',
            'Tapis de yoga',
            'Step platforms',
            'Swiss balls',
            'Câbles et poulies',
            'Leg press',
            'Rameur',
            'Stepper',
            'Smith Machine',
            'Squat Rack',
            'Pull-up bar',
        ]
        
        equipment_created = 0
        for name in equipment_list:
            obj, created = Equipement.objects.get_or_create(name=name)
            if created:
                equipment_created += 1
                self.stdout.write(f'  ✅ Created: {name}')
            else:
                self.stdout.write(f'  ⏭️  Already exists: {name}')
        
        # ==========================================
        # SERVICES
        # ==========================================
        service_choices = ['douches', 'wifi', 'climatisation', 'parking']
        services_created = 0
        
        for choice in service_choices:
            obj, created = Service.objects.get_or_create(nom=choice)
            if created:
                services_created += 1
                self.stdout.write(f'  ✅ Created service: {obj.get_nom_display()}')
            else:
                self.stdout.write(f'  ⏭️  Service already exists: {obj.get_nom_display()}')
        
        # ==========================================
        # SUMMARY
        # ==========================================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'✅ Seeding complete!'))
        self.stdout.write(self.style.SUCCESS(f'📦 Equipment: {equipment_created} created, {len(equipment_list) - equipment_created} already existed'))
        self.stdout.write(self.style.SUCCESS(f'🔧 Services: {services_created} created, {len(service_choices) - services_created} already existed'))
        self.stdout.write(self.style.SUCCESS('=' * 50))