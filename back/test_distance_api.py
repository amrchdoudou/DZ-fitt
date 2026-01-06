import requests

# Test with user coordinates (Constantine)
lat = 36.2520
lng = 6.7208

print(f"Testing search with user coordinates: lat={lat}, lng={lng}")

try:
    # Test distances: 20km (should find only close ones), 50km, 200km
    for distance in [20, 50, 200]:
        print(f"\n=== Testing Distance Filter: {distance} km ===")
        response = requests.get('http://localhost:8000/api/salles/search/', params={
            'lat': lat,
            'lng': lng,
            'distance': distance
        })
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} gyms:")
            for gym in data:
                dist = gym.get('distance', -1)
                print(f"DEBUG: gym='{gym['nom']}' dist_val={dist} type={type(dist)}")
                
                # If distance is a string like "13.2 km", parse it?
                # The serializer usually returns the float or str representation.
                print(f"  - {gym['nom']}: {dist}")
        else:
            print(f"Error: {response.status_code}")

except Exception as e:
    print(f"Request failed: {e}")
