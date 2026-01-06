import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_filters():
    print("\n--- Testing /api/filters/ ---")
    try:
        response = requests.get(f"{BASE_URL}/filters/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Filter Keys:", list(data.keys()))
            print("Services:", data.get('services'))
            print("Equipment:", data.get('equipment'))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

def test_search_all():
    print("\n--- Testing /api/salles/search/ (No params) ---")
    try:
        response = requests.get(f"{BASE_URL}/salles/search/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} gyms")
            if len(data) > 0:
                print("First Gym:", json.dumps(data[0], indent=2))
    except Exception as e:
        print(f"Request failed: {e}")

def test_search_text():
    print("\n--- Testing /api/salles/search/ (Search Query) ---")
    try:
        # Assuming there is a gym with 'Fit' or similar in its name
        response = requests.get(f"{BASE_URL}/salles/search/", params={"search": "fit"})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} gyms matching 'fit'")
    except Exception as e:
        print(f"Request failed: {e}")

def test_search_distance():
    print("\n--- Testing /api/salles/search/ (Distance) ---")
    # Coordinates for Bejaia center approx
    params = {
        "lat": 36.7538,
        "lng": 5.0588,
        "distance": 10
    }
    try:
        response = requests.get(f"{BASE_URL}/salles/search/", params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} gyms within 10km of Bejaia")
            for gym in data:
                print(f"- {gym['nom']}: {gym.get('distance', 'N/A')} km")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_filters()
    test_search_all()
    test_search_text()
    test_search_distance()
