import os
import sys
import django
from django.test import RequestFactory
from django.conf import settings

# Add 'back' directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from app.views import UnifiedSalleSearchView
from app.models import Salle

def test_distance_filter():
    factory = RequestFactory()
    view = UnifiedSalleSearchView.as_view()

    # User location (Constantine)
    lat = 36.2520
    lng = 6.7208

    print(f"User Location: {lat}, {lng}")
    print("-" * 50)

    # Test cases: different distances
    distances = [10, 20, 50, 100, 200, None]

    for dist in distances:
        params = {
            'lat': lat,
            'lng': lng,
            'search': '' # Ensure search doesn't interfere
        }
        if dist is not None:
            params['distance'] = dist

        request = factory.get('/api/salles/search/', data=params)
        response = view(request)
        
        print(f"Testing Distance Filter: {dist} km")
        if response.status_code == 200:
            data = response.data
            print(f"Found {len(data)} gyms:")
            for gym in data:
                print(f"  - {gym['nom']}: {gym.get('distance', 'N/A')} km")
        else:
            print(f"Error: {response.status_code}")
        print("-" * 50)

if __name__ == '__main__':
    test_distance_filter()
