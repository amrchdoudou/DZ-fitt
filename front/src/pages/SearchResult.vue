<template>
  <div class="search-results-container">
    <Header />
    <!-- Filters Bar -->
     <div class="filters-bar">
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedDistance" @change="fetchGyms()" class="filter-select">
          <option value="">Distance</option>
          <!-- Load distance options from backend API -->
          <option v-for="distance in filterOptions.distances" :key="distance.value" :value="distance.value">
            {{ distance.label }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedEquipment" @change="fetchGyms()" class="filter-select">
          <option value="">Equipment</option>
          <!-- Load equipment options from backend API -->
          <option v-for="equipment in filterOptions.equipment" :key="equipment" :value="equipment">
            {{ equipment }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedServices" @change="fetchGyms()" class="filter-select">
          <option value="">Services</option>
          <!-- Load services options from backend API -->
          <option v-for="service in filterOptions.services" :key="service" :value="service">
            {{ service }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedDay" @change="fetchGyms()" class="filter-select">
          <option value="">Day</option>
          <option v-for="day in filterOptions.days" :key="day.value" :value="day.value">
            {{ day.label }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedTimePeriod" @change="fetchGyms()" class="filter-select">
          <option value="">Time Period</option>
          <option v-for="time in filterOptions.times" :key="time" :value="time">
            {{ time }}
          </option>
        </select>
        <!-- Optional specific time input -->
        <input 
          type="time" 
          v-model="specificTime" 
          @change="fetchGyms()" 
          class="filter-select" 
          style="margin-left:5px; width:auto;"
          title="Specific Time"
        />
      </div>
      <div class="filter-item">
        <span class="filter-icon">▼</span>
        <select v-model="selectedRating" @change="fetchGyms()" class="filter-select">
          <option value="">Rating</option>
          <!-- Load rating options from backend API -->
          <option v-for="rating in filterOptions.ratings" :key="rating.value" :value="rating.value">
            {{ rating.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <!-- Left Sidebar - Results List -->
      <div class="results-sidebar">
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text"
            placeholder="Search gyms..."
            class="search-input"
            @input="onSearchInput"
          >
          <div class="search-controls">
            <button v-if="searchQuery" @click="clearSearch" class="clear-btn" title="Clear">✕</button>
            <button @click="getUserLocation" class="locate-btn" title="Use my location">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/>
              </svg>
            </button>
          </div>
        </div>

        <!-- Show message before any search, then show results or no results -->
        <div v-if="!hasSearched && searchQuery === ''" class="empty-state">
          <div class="empty-icon">🔍</div>
          <p class="empty-text">Enter a gym name to search</p>
        </div>

        <div v-else-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Loading...</p>
        </div>

        <div v-else-if="filteredGyms.length === 0" class="no-results">
          No gyms found matching your criteria
        </div>

        <div v-else class="results-list">
          <div 
            v-for="gym in filteredGyms" 
            :key="gym.id" 
            class="result-item"
            :class="{ active: selectedGymId === gym.id }"
            @click="selectGym(gym)"
          >
            <div class="gym-logo-container">
              <img v-if="gym.logo && gym.logo !== '🏋️'" :src="gym.logo" :alt="gym.name" class="gym-logo-img" @error="handleImageError">
              <div v-else class="gym-logo-placeholder">🏋️</div>
            </div>
            <div class="gym-info">
              <h3 class="gym-name">{{ gym.name }}</h3>
              <div class="gym-meta">
                <span class="distance">{{ gym.distance }}</span>
                <span class="rating">★ {{ gym.rating }}</span>
              </div>
              <p class="gym-price">{{ gym.price }}</p>
              <div class="result-actions">
                <router-link :to="'/gym/' + gym.id" class="view-profile-btn" @click.stop>
                  View Profile
                </router-link>
                <button class="itinerary-btn" @click.stop="getRoute(gym.id)">
                  Itinerary
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side - Map -->
      <div class="map-container">
        <div id="map" class="map"></div>
      </div>
    </div>
  </div>
</template>


<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import Header from '../components/layouts/Header.vue';
import api from '../api';
import { cityCoordinates } from '../data/cityCoordinates';

export default {
  name: 'SearchResults',
  components: {
    Header
  },
  data() {
    return {
      searchQuery: '',
      selectedDistance: '',
      selectedEquipment: '',
      selectedServices: '',
      selectedDay: '',
      selectedTimePeriod: '',
      specificTime: '',
      selectedRating: '',
      selectedGymId: null,
      map: null,
      markers: {},
      locationMarker: null,
      locationCoordinates: null,
      gyms: [],
      loading: false,
      hasSearched: false,
      searchTimeout: null,
      filterOptions: {
        distances: [],
        equipment: [],
        services: [],
        days: [],
        times: [],
        ratings: []
      },
      cityCoordinates: cityCoordinates
    }
  },
  computed: {
    filteredGyms() {
      return this.gyms;
    }
  },
  methods: {
    handleImageError(e) {
      e.target.style.display = 'none';
      e.target.nextElementSibling.style.display = 'flex';
    },

    async fetchFilters() {
      try {
        const response = await api.getFilters();
        this.filterOptions = response.data;
      } catch (error) {
        console.error('[v0] Error fetching filters:', error);
      }
    },

    onSearchInput() {
      clearTimeout(this.searchTimeout);
      if (this.searchQuery.trim() === '') {
        this.hasSearched = false;
        this.gyms = [];
        this.removeLocationMarker();
        this.updateMapMarkers();
        return;
      }
      
      this.hasSearched = true;
      this.searchTimeout = setTimeout(async () => {
        await this.geolocationAddress();
        this.fetchGyms();
      }, 500);
    },

    async geolocationAddress() {
      try {
        const query = this.searchQuery.toLowerCase().trim();
        
        // Match "Ma position" or "Mon emplacement"
        if (query === 'ma position' || query === 'mon emplacement' || query === 'my location') {
          this.getUserLocation();
          return;
        }

        if (this.cityCoordinates[query]) {
          const coords = this.cityCoordinates[query];
          this.locationCoordinates = { lat: coords.lat, lng: coords.lng };
          this.addLocationMarker(coords.lat, coords.lng);
          this.updateMapBounds();
          return;
        }
        
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(this.searchQuery)},Algeria&format=json&limit=1&countrycodes=dz`
        );
        const results = await response.json();
        
        if (results && results.length > 0) {
          const lat = parseFloat(results[0].lat);
          const lon = parseFloat(results[0].lon);
          this.locationCoordinates = { lat, lng: lon };
          this.addLocationMarker(lat, lon);
          this.updateMapBounds();
        } else {
          console.error('[SearchResult] No location found for:', this.searchQuery);
        }
      } catch (error) {
        console.error('[SearchResult] Error geocoding address:', error);
      }
    },

    getUserLocation() {
      if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser");
        return;
      }

      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords;
          this.locationCoordinates = { lat: latitude, lng: longitude };
          this.searchQuery = 'Ma position';
          this.hasSearched = true;
          this.addLocationMarker(latitude, longitude);
          this.updateMapBounds();
          this.fetchGyms(); // Refresh search based on new location
        },
        (error) => {
          console.error("Error getting location:", error);
          alert("Unable to retrieve your location. Using default view.");
        }
      );
    },

    addLocationMarker(lat, lng) {
      console.log('[SearchResult] Adding location marker at:', lat, lng);
      
      // Remove previous marker but KEEP coordinates in state
      if (this.locationMarker) {
        this.map.removeLayer(this.locationMarker);
        this.locationMarker = null;
      }
      
      // Use a custom red marker icon
      const locationIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNiIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDM2IDQ4Ij48cGF0aCBmaWxsPSIjRjkxOTFDIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgZD0iTTEgMC41QzEgMCAwIDEgMCAydjI0YzAgMTIgOCAyMCAxNiAzMmM4IC0xMiAxNiAtMjAgMTYgLTMyVjJjMCAtMSAtMSAtMiAtMiAtMkgxYy0wLjUgMCAtMSAwLjUgLTEgMXptMTAgMTJjMCAzLjMgMi43IDYgNiA2czYgLTIuNyA2IC02YzAgLTMuMyAtMi43IC02IC02IC02cy02IDIuNyAtNiA2eiIvPjwvc3ZnPg==',
        iconSize: [36, 48],
        iconAnchor: [18, 48],
        popupAnchor: [0, -48]
      });

      this.locationMarker = L.marker([lat, lng], {
        icon: locationIcon,
        title: 'Search Location',
        zIndexOffset: 1000
      }).addTo(this.map);
      
      console.log('[SearchResult] Location marker created:', this.locationMarker);
      
      // Center map on user location with higher zoom
      this.map.setView([lat, lng], 15);
      console.log('[SearchResult] Map centered on location with zoom 15');
    },

    removeLocationMarker(clearCoords = true) {
      if (this.locationMarker) {
        this.map.removeLayer(this.locationMarker);
        this.locationMarker = null;
      }
      if (clearCoords) {
        this.locationCoordinates = null;
      }
    },

    updateMapBounds() {
      const bounds = L.latLngBounds();
      
      if (this.locationCoordinates) {
        bounds.extend([this.locationCoordinates.lat, this.locationCoordinates.lng]);
      }
      
      this.filteredGyms.forEach(gym => {
        bounds.extend([gym.lat, gym.lng]);
      });
      
      if (bounds.isValid()) {
        this.map.fitBounds(bounds, { padding: [100, 100], maxZoom: 16 });
      }
    },

    async fetchGyms(arg = null) {
      try {
        this.loading = true;
        const params = {};
        
        // Determine coordinates to use
        let coordinates = null;
        
        if (arg && typeof arg.lat !== 'undefined') {
            // Arg is a coordinate object
            coordinates = arg;
        } else {
            // Arg is null (from template) or not coordinates
            // Fallback to stored location
            coordinates = this.locationCoordinates;
        }

        // Final fallback: Check URL query params if we still don't have coordinates
        if (!coordinates && this.$route.query.lat && this.$route.query.lng) {
            coordinates = {
                lat: parseFloat(this.$route.query.lat),
                lng: parseFloat(this.$route.query.lng)
            };
        }
        
        console.log('[SearchResult] Using coordinates:', coordinates);
        
        // Only add search param if it's not the default "Ma position" text
        if (this.searchQuery && this.searchQuery !== 'Ma position') {
          params.search = this.searchQuery;
        }
        
        if (this.selectedDistance) params.distance = this.selectedDistance;
        if (this.selectedEquipment) params.equipment = this.selectedEquipment;
        if (this.selectedServices) params.services = this.selectedServices;
        if (this.selectedRating) params.rating = this.selectedRating;
        
        if (this.selectedDay) params.day = this.selectedDay;
        
        if (this.specificTime) {
            params.time = this.specificTime;
        } else if (this.selectedTimePeriod) {
            params.time = this.selectedTimePeriod;
        }
        
        // Add location coordinates if available
        if (coordinates) {
          console.log('[SearchResult] Adding coordinates to params');
          params.lat = coordinates.lat;
          params.lng = coordinates.lng;
          // Add default distance of 100km if not specified
          if (!params.distance) {
            params.distance = 100;
          }
        }

        console.log('[SearchResult] Fetching gyms with params:', params);
        const response = await api.searchGyms(params);
        console.log('[SearchResult] API response:', response.data);
        
        // Transform backend data to component format
        this.gyms = response.data.map(gym => ({
          id: gym.id,
          name: gym.nom || 'Gym',
          logo: gym.logo || '🏋️',
          distance: gym.distance ? `${gym.distance.toFixed(1)} km` : 'N/A',
          rating: gym.note_moyenne ? gym.note_moyenne.toFixed(1) : '0.0',
          price: gym.prix_moyen || 'Prix non disponible',
          lat: parseFloat(gym.latitude) || 36.7538,
          lng: parseFloat(gym.longitude) || 5.0588
        }));
        
        console.log('[SearchResult] Transformed gyms:', this.gyms);
        this.updateMapMarkers();
        this.updateMapBounds();
      } catch (error) {
        console.error('Error fetching gyms:', error);
        this.gyms = [];
      } finally {
        this.loading = false;
      }
    },

    clearSearch() {
      this.searchQuery = '';
      this.hasSearched = false;
      this.gyms = [];
      this.selectedGymId = null;
      this.removeLocationMarker();
      this.updateMapMarkers();
    },

    selectGym(gym) {
      this.selectedGymId = gym.id;
      // Update markers without clearing everything if possible, or just call updateMapMarkers
      this.updateMapMarkers();
      if (this.map && this.markers[gym.id]) {
        // Find coordinates of selected gym
        const gymData = this.gyms.find(g => g.id === gym.id);
        if (gymData) {
            this.map.setView([gymData.lat, gymData.lng], 16);
            this.markers[gym.id].openPopup();
        }
      }
    },

    async getRoute(gymId) {
      try {
        console.log('[SearchResult] Fetching directions for gym:', gymId);
        
        // Pass origin coordinates if we have a search location
        const originLat = this.locationCoordinates ? this.locationCoordinates.lat : null;
        const originLng = this.locationCoordinates ? this.locationCoordinates.lng : null;
        
        const response = await api.getDirections(gymId, 'driving', originLat, originLng);
        if (response.data && response.data.google_maps_url) {
          window.open(response.data.google_maps_url, '_blank');
        } else if (response.data && response.data.transport_modes) {
          // Fallback to driving if all_modes was somehow used or default
          const drivingUrl = response.data.transport_modes.driving?.url;
          if (drivingUrl) window.open(drivingUrl, '_blank');
        } else {
          console.warn('[SearchResult] No directions URL found in response');
        }
      } catch (error) {
        console.error('Error getting directions:', error);
      }
    },

    updateMapMarkers() {
      if (!this.map) return;
      
      console.log('[SearchResult] Updating markers for', this.filteredGyms.length, 'gyms');

      // Remove markers that are no longer in the filtered list
      const currentGymIds = new Set(this.filteredGyms.map(g => g.id));
      Object.keys(this.markers).forEach(id => {
        if (!currentGymIds.has(Number(id))) {
          this.map.removeLayer(this.markers[id]);
          delete this.markers[id];
        }
      });

      if (this.filteredGyms.length === 0) {
        this.map.setView([36.7538, 5.0588], 12);
        return;
      }

      const activeGymIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNiIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDM2IDQ4Ij48cGF0aCBmaWxsPSIjMDc4YzQ0IiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgZD0iTTEgMC41QzEgMCAwIDEgMCAydjI0YzAgMTIgOCAyMCAxNiAzMmM4IC0xMiAxNiAtMjAgMTYgLTMyVjJjMCAtMSAtMSAtMiAtMiAtMkgxYy0wLjUgMCAtMSAwLjUgLTEgMXptMTAgMTJjMCAzLjMgMi43IDYgNiA2czYgLTIuNyA2IC02YzAgLTMuMyAtMi43IC02IC02IC02cy02IDIuNyAtNiA2eiIvPjwvc3ZnPg==',
        iconSize: [36, 48],
        iconAnchor: [18, 48],
        popupAnchor: [0, -48]
      });

      const inactiveGymIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNiIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDM2IDQ4Ij48cGF0aCBmaWxsPSIjMDA1MmNjIiBzdHJva2U9IiNmZmZmZmYiIHN0cm9rZS13aWR0aD0iMiIgZD0iTTEgMC41QzEgMCAwIDEgMCAydjI0YzAgMTIgOCAyMCAxNiAzMmM4IC0xMiAxNiAtMjAgMTYgLTMyVjJjMCAtMSAtMSAtMiAtMiAtMkgxYy0wLjUgMCAtMSAwLjUgLTEgMXptMTAgMTJjMCAzLjMgMi43IDYgNiA2czYgLTIuNyA2IC02YzAgLTMuMyAtMi43IC02IC02IC02cy02IDIuNyAtNiA2eiIvPjwvc3ZnPg==',
        iconSize: [36, 48],
        iconAnchor: [18, 48],
        popupAnchor: [0, -48]
      });

      this.filteredGyms.forEach(gym => {
        const isSelected = this.selectedGymId === gym.id;
        const markerIcon = isSelected ? activeGymIcon : inactiveGymIcon;
        
        if (this.markers[gym.id]) {
          // Update existing marker
          this.markers[gym.id].setIcon(markerIcon);
          this.markers[gym.id].setZIndexOffset(isSelected ? 600 : 500);
        } else {
          // Create new marker
          const latLng = L.latLng(gym.lat, gym.lng);
          const marker = L.marker(latLng, {
            icon: markerIcon,
            zIndexOffset: isSelected ? 600 : 500
          }).addTo(this.map);
          
          marker.bindPopup(`
            <div class="modern-popup">
              <h3 class="popup-title">${gym.name}</h3>
              <div class="popup-info">
                <span class="popup-distance">📍 ${gym.distance}</span>
                <span class="popup-rating">⭐ ${gym.rating}</span>
              </div>
              <p class="popup-price">${gym.price}</p>
              <div class="popup-actions">
                <a href="/gym/${gym.id}" class="popup-btn view-btn">View Profile</a>
                <button onclick="window.handlePopupItinerary(${gym.id})" class="popup-btn route-btn">Itinerary</button>
              </div>
            </div>
          `, {
            closeButton: true,
            className: 'custom-popup'
          });
          
          this.markers[gym.id] = marker;

          // Add hover and click interactions
          marker.on('mouseover', (e) => {
            e.target.openPopup();
          });
          
          marker.on('mouseout', (e) => {
            if (this.selectedGymId !== gym.id) {
              e.target.closePopup();
            }
          });

          marker.on('click', () => {
            this.selectGym(gym);
          });

          // Reset selection when popup is closed (manually or by switching)
          marker.on('popupclose', () => {
            if (this.selectedGymId === gym.id) {
              this.selectedGymId = null;
              this.updateMapMarkers();
            }
          });
        }
      });
    },

    initMap() {
      this.map = L.map('map', {
        zoomControl: true,
        attributionControl: true,
        scrollWheelZoom: true,
        dragging: true,
        touchZoom: true
      }).setView([36.7538, 5.0588], 13);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
        minZoom: 3,
        className: 'map-tiles'
      }).addTo(this.map);

      this.map.invalidateSize();
    }
  },
  mounted() {
    // Expose method for popup buttons
    window.handlePopupItinerary = (id) => {
      this.getRoute(id);
    };

    this.fetchFilters();
    this.$nextTick(() => {
      this.initMap();
      
      const { search, lat, lng } = this.$route.query;
      console.log('[SearchResult] Route query params:', { search, lat, lng });
      
      if (lat && lng) {
        console.log('[SearchResult] Geolocation mode detected');
        this.searchQuery = search || 'Ma position';
        const coords = { 
          lat: parseFloat(lat), 
          lng: parseFloat(lng) 
        };
        this.locationCoordinates = coords;
        this.hasSearched = true;
        
        // Wait for map to be fully initialized before adding marker
        setTimeout(() => {
          console.log('[SearchResult] Calling addLocationMarker');
          this.addLocationMarker(coords.lat, coords.lng);
          // Pass coordinates directly to fetchGyms
          this.fetchGyms(coords);
        }, 100);
      } else if (search) {
        console.log('[SearchResult] Text search mode detected');
        this.searchQuery = search;
        this.hasSearched = true;
        this.onSearchInput();
      }
    });
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.search-results-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: white;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.filters-bar {
  background: white;
  padding: 16px 32px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  gap: 12px;
  max-width: 100%;
  flex-wrap: wrap;
  align-items: center;
}

.filter-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  position: relative;
  background: #FAFAFA;
  padding: 12px 24px;
  border-radius: 20px;
  border: 1px solid  #d0d0d0;
  height: 34px;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.filter-item:hover {
  border-color: #b0b0b0;
  background: #fafafa;
}

.filter-select {
  background: transparent;
  border: none;
  font-size: 13px;
  color: #333333;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  padding: 0 4px;
  appearance: none;
  text-align: center;
}

.filter-select:hover {
  color: #1e88e5;
}

.filter-select option {
  background: white;
  color: #333;
  font-weight: 500;
  padding: 8px;
}

.filter-icon {
  position: absolute;
  left: 13px;
  font-size: 9px;
  opacity: 0.6;
  pointer-events: none;
  color: #666;
  font-weight: bold;
}

.main-content {
  display: flex;
  gap: 24px;
  padding: 16px 32px 32px 32px;
  flex: 1;
  overflow: hidden;
}

.results-sidebar {
  flex: 0 0 378px;
  border-radius: 8px;
  background: white;
  border-right: 1px dotted #b0b0b0;
  padding: 16px 12px;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.results-sidebar::-webkit-scrollbar,
.results-list::-webkit-scrollbar {
  width: 6px;
}

.results-sidebar::-webkit-scrollbar-track,
.results-list::-webkit-scrollbar-track {
  background: transparent;
}

.results-sidebar::-webkit-scrollbar-thumb,
.results-list::-webkit-scrollbar-thumb {
  background: #d8d8d8;
  border-radius: 3px;
}

.search-box {
  position: relative;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.search-input {
  width: 100%;
  padding: 12px 80px 12px 16px;
  border: 1px solid #E0E0E0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
  background: rgba(250, 250, 250, 0.8);
  color: #333;
}

.search-input:focus {
  border-color: #1e88e5;
  background: white;
  box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.08);
}

.search-input::placeholder {
  color: #bbb;
  font-size: 12px;
}

.search-controls {
  position: absolute;
  right: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-btn, .locate-btn {
  background: none !important;
  border: none !important;
  cursor: pointer;
  padding: 6px;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: none !important;
  transform: none !important;
}

.clear-btn:hover {
  color: #666;
}

.locate-btn:hover {
  color: #0940BE;
}

.empty-state {
  text-align: center;
  padding: 50px 12px;
  color: #bbb;
}

.empty-icon {
  font-size: 32px;
  margin-bottom: 8px;
  opacity: 0.5;
}

.empty-text {
  font-size: 11px;
  font-weight: 500;
  color: #aaa;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 12px;
  color: #999;
  gap: 8px;
  font-size: 11px;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid #f0f0f0;
  border-top-color: #1e88e5;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-results {
  text-align: center;
  padding: 30px 12px;
  color: #bbb;
  font-size: 11px;
}

.results-list, .empty-state, .loading-state, .no-results {
  flex: 1;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #d8d8d8 transparent;
  padding-right: 4px;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  border: 1px solid #F0F0F0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.result-item:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border-color: #E0E0E0;
  transform: translateY(-2px);
}

.result-item.active {
  border-color: transparent;
  background: #e8f1f8;
  box-shadow: none;
}

.gym-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background: #F5F7FA;
  border-radius: 8px;
  flex-shrink: 0;
  border: 1px solid #EEE;
}

.gym-logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 3px;
}

.gym-logo {
  font-size: 18px;
}

.gym-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
}

.gym-name {
  font-size: 15px;
  font-weight: 700;
  color: #040B1A;
  margin-bottom: 4px;
  line-height: 1.2;
}

.gym-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #65697A;
  margin-bottom: 4px;
}

.distance {
  color: #e91e63;
  font-weight: 600;
  font-size: 12px;
}

.rating {
  color: #666;
  font-size: 12px;
}

.gym-price {
  font-size: 11px;
  color: #65697A;
  margin: 4px 0 8px 0;
}

.result-actions {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.view-profile-btn, .itinerary-btn {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  border: 1px solid transparent;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.view-profile-btn {
  background: #0940BE;
  color: white;
}

.view-profile-btn:hover {
  background: #0734a0;
  transform: translateY(-1px);
}

.itinerary-btn {
  background: white;
  color: #0940BE;
  border-color: #0940BE;
}

.itinerary-btn:hover {
  background: #f0f4ff;
  transform: translateY(-1px);
}

/* Modern Popup Styles */
:deep(.modern-popup) {
  min-width: 220px;
  padding: 4px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

:deep(.popup-title) {
  font-size: 16px;
  font-weight: 700;
  color: #040B1A;
  margin: 0 0 8px 0;
  line-height: 1.2;
}

:deep(.popup-info) {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
}

:deep(.popup-distance) {
  color: #E91E63;
  font-size: 13px;
  font-weight: 600;
}

:deep(.popup-rating) {
  color: #FF9800;
  font-size: 13px;
  font-weight: 600;
}

:deep(.popup-price) {
  color: #65697A;
  font-size: 12px;
  margin-bottom: 12px;
}

:deep(.popup-actions) {
  display: flex;
  gap: 8px;
}

:deep(.popup-btn) {
  flex: 1;
  padding: 8px 0;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-align: center;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

:deep(.view-btn) {
  background: #0940BE;
  color: white;
}

:deep(.route-btn) {
  background: #F0F4FF;
  color: #0940BE;
}

:deep(.popup-btn:hover) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.map-container {
  flex: 1;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  min-height: 500px;
  border: none;
}

#map {
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: #e8f0f7;
}

@media (max-width: 1024px) {
  .main-content {
    flex-direction: column;
  }

  .results-sidebar {
    flex: 0 0 auto;
    max-height: 350px;
    border-right: none;
    border-bottom: 1px dotted #b0b0b0;
  }

  .map-container {
    flex: 1;
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .filters-bar {
    gap: 10px;
    overflow-x: auto;
    padding: 10px 12px;
  }

  .results-sidebar {
    max-height: 280px;
  }
}

:deep(.leaflet-popup-content-wrapper) {
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e0e0e0;
  padding: 8px 10px;
}

:deep(.leaflet-popup-tip) {
  background-color: white;
  border: 1px solid #e0e0e0;
}

:deep(.leaflet-control-zoom) {
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  background: white !important;
}

:deep(.leaflet-control-zoom-in),
:deep(.leaflet-control-zoom-out) {
  color: #1e88e5;
  font-weight: bold;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 16px;
}

:deep(.leaflet-control-zoom-in:hover),
:deep(.leaflet-control-zoom-out:hover) {
  background-color: #f5f5f5 !important;
}

</style>
