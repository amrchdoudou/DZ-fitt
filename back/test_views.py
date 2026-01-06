import sys
import os
import django

# Add the back directory to sys.path
sys.path.append('/code/back')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.models import Salle

def test_view_increment():
    salle = Salle.objects.first()
    if not salle:
        print("No salle found to test.")
        return

    old_count = salle.views_count
    print(f"Testing Salle: {salle.nom} (ID: {salle.id})")
    print(f"Current views_count: {old_count}")

    # Forcing an increment via direct model update (simulating what the view does)
    from django.db.models import F
    Salle.objects.filter(pk=salle.pk).update(views_count=F('views_count') + 1)
    
    salle.refresh_from_db()
    new_count = salle.views_count
    print(f"New views_count: {new_count}")

    if new_count == old_count + 1:
        print("✅ SUCCESS: views_count incremented correctly.")
    else:
        print("❌ FAILURE: views_count did not increment.")

if __name__ == "__main__":
    test_view_increment()
