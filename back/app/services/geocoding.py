# app/services/geocoding.py

import requests
import time
from django.core.cache import cache

class GeocodingService:
    """
    Service de géocodage utilisant Nominatim (OpenStreetMap)
    API gratuite - limite : 1 requête/seconde
    """
    
    BASE_URL = "https://nominatim.openstreetmap.org/search"
    
    @staticmethod
    def geocode_address(address, country="Algeria"):
        """
        Convertit une adresse en coordonnées GPS
        
        Args:
            address (str): Adresse complète (ex: "12 Rue Didouche, Alger")
            country (str): Pays pour améliorer la précision
            
        Returns:
            dict: {
                'success': bool,
                'latitude': float,
                'longitude': float,
                'display_name': str,  # Adresse formatée par Nominatim
                'address_details': dict,
                'error': str (si échec)
            }
        """
        # Vérifier le cache pour éviter de refaire la même requête
        cache_key = f"geocode_{address}_{country}"
        cached_result = cache.get(cache_key)
        if cached_result:
            print(f"✅ Géocodage depuis cache: {address}")
            return cached_result
        
        try:
            # Paramètres de la requête Nominatim
            # NOTE: 'country' n'est pas un paramètre valide pour /search, on l'ajoute à l'adresse
            search_query = f"{address}, {country}"
            
            params = {
                'q': search_query,          # Adresse complète + Pays
                'format': 'json',           # Format de réponse
                'limit': 1,                 # Un seul résultat (le meilleur)
                'addressdetails': 1,        # Inclure détails (ville, wilaya, etc.)
            }
            
            # Headers OBLIGATOIRES pour Nominatim
            headers = {
                'User-Agent': 'DZ-Fit/1.0 (contact@dzfit.com)'
            }
            
            print(f"🔍 Géocodage de: {search_query}")
            
            # Appel API
            response = requests.get(
                GeocodingService.BASE_URL,
                params=params,
                headers=headers,
                timeout=10  # Timeout de 10 secondes
            )
            
            # Vérifier si la requête a réussi
            if response.status_code != 200:
                return {
                    'success': False,
                    'error': f"Erreur API Nominatim: {response.status_code}"
                }
            
            data = response.json()
            
            # Vérifier si on a trouvé des résultats
            if not data or len(data) == 0:
                return {
                    'success': False,
                    'error': "Adresse introuvable. Vérifiez l'orthographe."
                }
            
            # Récupérer le premier (meilleur) résultat
            result = data[0]
            
            geocode_result = {
                'success': True,
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'display_name': result['display_name'],
                'address_details': result.get('address', {}),
            }
            
            print(f"✅ Géocodage réussi: {geocode_result['latitude']}, {geocode_result['longitude']}")
            
            # Mettre en cache pour 24 heures
            cache.set(cache_key, geocode_result, 60 * 60 * 24)
            
            # IMPORTANT : Respecter la limite de 1 requête/seconde
            time.sleep(1)
            
            return geocode_result
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': "Le service de géocodage ne répond pas. Réessayez dans quelques instants."
            }
        except Exception as e:
            print(f"❌ Erreur géocodage: {str(e)}")
            return {
                'success': False,
                'error': f"Erreur: {str(e)}"
            }
    
    @staticmethod
    def get_google_maps_directions_url(latitude, longitude, salle_nom="", origin_lat=None, origin_lng=None):
        """
        Génère l'URL Google Maps pour obtenir l'itinéraire vers une salle
        
        Args:
            latitude (float): Latitude de la salle (destination)
            longitude (float): Longitude de la salle (destination)
            salle_nom (str): Nom de la salle
            origin_lat (float): Latitude de départ (optionnel)
            origin_lng (float): Longitude de départ (optionnel)
        """
        base_url = "https://www.google.com/maps/dir/"
        
        # Destination (ALWAYS use coordinates for precision)
        destination = f"{latitude},{longitude}"
        
        # Origin
        origin = ""
        if origin_lat and origin_lng:
            origin = f"&origin={origin_lat},{origin_lng}"
        
        # Construire l'URL complète
        full_url = f"{base_url}?api=1&destination={destination}{origin}&travelmode=driving"
        
        return full_url
    
    @staticmethod
    def get_multiple_transport_modes(latitude, longitude, salle_nom="", origin_lat=None, origin_lng=None):
        """
        Génère plusieurs liens pour différents modes de transport
        """
        base_url = "https://www.google.com/maps/dir/"
        destination = f"{latitude},{longitude}"
        
        origin = ""
        if origin_lat and origin_lng:
            origin = f"&origin={origin_lat},{origin_lng}"
            
        return {
            'driving': f"{base_url}?api=1&destination={destination}{origin}&travelmode=driving",
            'walking': f"{base_url}?api=1&destination={destination}{origin}&travelmode=walking",
            'bicycling': f"{base_url}?api=1&destination={destination}{origin}&travelmode=bicycling",
            'transit': f"{base_url}?api=1&destination={destination}{origin}&travelmode=transit",
        }


# ===============================
# FONCTION UTILITAIRE
# ===============================

def geocode_and_save_salle(salle):
    """
    Géocode une salle et met à jour ses coordonnées automatiquement
    
    Cette fonction est appelée automatiquement quand un gérant crée/modifie une salle
    
    Args:
        salle (Salle): Instance du modèle Salle
        
    Returns:
        dict: Résultat du géocodage
    """
    # Construire l'adresse complète à partir des champs séparés
    address_parts = []
    
    if salle.rue:
        address_parts.append(salle.rue)
    if salle.ville:
        address_parts.append(salle.ville)
    if salle.wilaya:
        address_parts.append(salle.wilaya)
    
    # Vérifier qu'on a au moins une partie de l'adresse
    if not address_parts:
        return {
            'success': False,
            'error': 'Adresse incomplète. Au minimum, la ville est requise.'
        }
    
    # Joindre les parties avec des virgules
    full_address = ", ".join(address_parts)
    
    print(f"📍 Adresse à géocoder: {full_address}")
    
    # Appeler le service de géocodage
    result = GeocodingService.geocode_address(full_address)
    
    if result['success']:
        # ✅ Mettre à jour les coordonnées de la salle
        salle.latitude = result['latitude']
        salle.longitude = result['longitude']
        
        # Optionnel : améliorer les données d'adresse avec les infos de Nominatim
        address_details = result.get('address_details', {})
        if address_details:
            # Si ville/wilaya sont vides, on les remplit avec les données de Nominatim
            if not salle.ville and address_details.get('city'):
                salle.ville = address_details.get('city')
            
            if not salle.wilaya and address_details.get('state'):
                salle.wilaya = address_details.get('state')
            
            if not salle.codePostal and address_details.get('postcode'):
                salle.codePostal = address_details.get('postcode')
        
        # Sauvegarder la salle avec les nouvelles coordonnées
        salle.save()
        
        print(f"✅ Salle '{salle.nom}' géocodée: {result['latitude']}, {result['longitude']}")
        
        return {
            'success': True,
            'latitude': result['latitude'],
            'longitude': result['longitude'],
            'display_name': result['display_name']
        }
    else:
        print(f"❌ Échec géocodage: {result.get('error')}")
        return result