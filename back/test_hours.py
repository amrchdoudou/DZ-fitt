import requests
import datetime

def test_hours_filter():
    base_url = 'http://localhost:8000/api/salles/search/'
    
    print(f"Current Time: {datetime.datetime.now()}")
    
    # Test 'Ouvert maintenant'
    print("\n--- Testing 'Ouvert maintenant' ---")
    try:
        r = requests.get(base_url, params={'hours': 'Ouvert maintenant'})
        if r.status_code == 200:
            gyms = r.json()
            print(f"Found {len(gyms)} gyms open now.")
            for g in gyms:
                print(f"- {g['nom']}")
        else:
            print(f"Error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"Request failed: {e}")

    # Test 'Matin'
    print("\n--- Testing 'Matin' ---")
    try:
        r = requests.get(base_url, params={'hours': 'Matin'})
        if r.status_code == 200:
            gyms = r.json()
            print(f"Found {len(gyms)} gyms open in morning.")
        else:
            print(f"Error {r.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    test_hours_filter()
