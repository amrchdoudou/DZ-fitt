<template>
  <div class="product-card-container">
    <div v-if="loading" class="loading-state">
      <p>Chargement...</p>
    </div>

    <!-- Product Card / Header Section -->
    <div v-else-if="gym" class="product-card">
      
      <!-- Cover Section -->
      <div class="cover-section">
        <div 
          class="cover-image" 
          :style="{ backgroundImage: gym.photo_couverture ? `url(${gym.photo_couverture})` : 'none', backgroundColor: '#eef2ff' }"
        >
          <div v-if="!gym.photo_couverture" class="cover-placeholder"></div>
        </div>

        <div class="avatar-container">
          <div class="avatar">
            <img 
              v-if="gym.logo" 
              :src="gym.logo" 
              :alt="gym.nom"
              class="avatar-img"
            />
            <div v-else class="avatar-placeholder">
              {{ gym.nom?.charAt(0) || 'G' }}
            </div>
          </div>
        </div>
      </div>

      <!-- Info Section -->
      <div class="info-section">
        <div class="header-row">
            <h1 class="gym-name">{{ gym.nom }}</h1>
            <a 
              v-if="gym.latitude && gym.longitude" 
              :href="directionsUrl" 
              target="_blank" 
              class="direction-btn"
            >
              Get Directions ↗
            </a>
        </div>

        <div class="details-row">
            <span v-if="gym.distance" class="distance-tag">{{ gym.distance }} km away</span>
            <span class="rating">
                <span class="star">⭐</span> {{ gym.note_moyenne ? Number(gym.note_moyenne).toFixed(1) : 'N/A' }}
            </span>
            
            <a 
               v-if="gym.latitude && gym.longitude"
               :href="`https://www.google.com/maps/search/?api=1&query=${gym.latitude},${gym.longitude}`" 
               target="_blank"
               class="location-link"
            >
                📍 {{ gym.ville }}{{ gym.wilaya ? ', ' + gym.wilaya : '' }}
            </a>
            <span v-else class="location">
                 📍 {{ gym.ville }}{{ gym.wilaya ? ', ' + gym.wilaya : '' }}
            </span>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, computed, onMounted } from 'vue'

const props = defineProps({
  gym: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const userLocation = ref(null);

onMounted(() => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        userLocation.value = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      },
      (error) => {
        console.log('Geolocation not available or denied', error);
      }
    );
  }
});

const directionsUrl = computed(() => {
  if (!props.gym || !props.gym.latitude || !props.gym.longitude) return '#';
  
  const dest = `${props.gym.latitude},${props.gym.longitude}`;
  
  if (userLocation.value) {
    return `https://www.google.com/maps/dir/?api=1&origin=${userLocation.value.lat},${userLocation.value.lng}&destination=${dest}&travelmode=driving`;
  }
  
  // Fallback if no user location
  return `https://www.google.com/maps/dir/?api=1&destination=${dest}`;
});
</script>

<style scoped>
.product-card-container {
  width: 100%;
  max-width: 1200px; /* Increased max-width to match new layout constraints */
  margin: 0 auto;
  padding: 0; 
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.product-card {
  background: white;
  border-radius: 0 0 12px 12px;
  overflow: visible; /* Changed to visible to allow avatar overflow if needed differently */
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  font-family: 'Inter', system-ui, sans-serif;
  padding-bottom: 24px;
  margin-bottom: 24px;
}

/* COVER & AVATAR */
.cover-section {
  position: relative;
  width: 100%;
  height: 200px; /* Reduced height as requested */
  margin-bottom: 0px; 
}

.cover-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 12px 12px 0 0; /* Rounded top corners only if card is rounded */
  position: relative;
}

/* Dark overlay for text readability if text is on cover */
.cover-image::after {
  content: '';
  position: absolute;
  top: 0; 
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.6));
  border-radius: 12px 12px 0 0;
}

.cover-placeholder {
  width: 100%;
  height: 100%;
  background: #1a1a1a; /* Dark background as in reference */
}

.avatar-container {
  position: absolute;
  bottom: -40px; /* Halfway out */
  left: 40px;
  width: 140px; /* Larger avatar */
  height: 140px;
  border-radius: 50%;
  border: 4px solid #1a1a1a; /* Dark border to match dark theme/background */
  background: #000;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  overflow: hidden;
  z-index: 10;
}

.avatar {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #000;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-size: 48px;
  font-weight: 700;
  color: #B3F90F; /* Brand color */
}

/* INFO SECTION */
.info-section {
  padding: 50px 40px 10px 40px; /* Top padding clears avatar */
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
}

.gym-name {
  font-size: 32px;
  font-weight: 800;
  color: #1f2937;
  margin: 0;
}

.details-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
}

.location, .rating, .phone, .location-link {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 15px;
  font-weight: 500;
}

.location, .phone {
  color: #4b5563;
}

.location-link {
  color: #0940BE;
  text-decoration: none;
  transition: color 0.2s;
}

.location-link:hover {
  text-decoration: underline;
  color: #073092;
}

.distance-tag {
    background: #ffe4e6;
    color: #e11d48;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.rating {
  color: #1f2937;
  font-weight: 600;
}

.star {
  color: #fbbf24;
}

.direction-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #0940BE;
  color: white;
  padding: 10px 20px;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.direction-btn:hover {
  background-color: #073092;
}

.description {
  color: #6b7280;
  line-height: 1.6;
  font-size: 15px;
  max-width: 800px;
  margin-top: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .cover-section {
    height: 180px;
  }
  
  .avatar-container {
    left: 20px;
    width: 100px;
    height: 100px;
    bottom: -30px;
  }
  
  .info-section {
    padding: 40px 20px 20px 20px;
  }
  
  .gym-name {
    font-size: 24px;
  }
  
  .actions-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 12px;
  }
}
</style>
