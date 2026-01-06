<template>
  <section class="hero-section">
    <!-- Background overlay -->
    <div class="hero-background">
      <img
        :src="landingBg"
        class="background-image"
        alt="Gym background"
      />
      <div class="background-overlay"></div>
    </div>

    <!-- Hero content -->
    <div class="hero-content">
      <!-- Main heading -->
      <div class="hero-text-container">
        <!-- Main text -->
        <h1 class="hero-title" v-html="$i18n.t('hero.title').replace('\n', '<br>')"></h1>
      </div>

      <!-- Subtitle -->
      <p class="hero-subtitle">
        {{ $i18n.t('hero.subtitle') }}
      </p>

      <!-- Search box -->
      <div class="search-container">
        <form @submit.prevent="handleSearch" class="search-form">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$i18n.t('hero.placeholder')"
            class="search-input"
          />
          <button type="submit" class="search-button">
            {{ $i18n.t('hero.search_btn') }}
          </button>
        </form>
        <button @click="useLocation" class="location-button">
          📍 {{ $i18n.t('hero.location_btn') }}
        </button>
      </div>
    </div>

    <!-- Wave decoration -->
    <div class="wave-decoration">
      <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0L60 10C120 20 240 40 360 46.7C480 53 600 47 720 43.3C840 40 960 40 1080 46.7C1200 53 1320 67 1380 73.3L1440 80V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z" fill="#B3F90F"/>
      </svg>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { i18n } from '../../i18n.js'
import landingBg from '../../images/gym bg.jpg'

const router = useRouter()
const searchQuery = ref('')

const $i18n = i18n;

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/SearchResult',
      query: { search: searchQuery.value.trim() }
    })
  } else {
    router.push({ path: '/SearchResult' })
  }
}

const useLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        router.push({
          path: '/SearchResult',
          query: { 
            lat: position.coords.latitude, 
            lng: position.coords.longitude,
            search: 'Ma position'
          }
        })
      },
      (error) => {
        console.error("Error getting location:", error)
        alert("Impossible de récupérer votre position. Veuillez entrer une adresse manuellement.")
      }
    )
  } else {
    alert("La géolocalisation n'est pas supportée par votre navigateur.")
  }
}
</script>

<style scoped>
.hero-section {
  position: relative;
  width: 100%;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px 100px;
  overflow: hidden;
  background-color: #0940BE;
}

.hero-background {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
}

.background-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(9, 64, 190, 0.7), rgba(9, 64, 190, 0.5));
}

.hero-content {
  position: relative;
  z-index: 10;
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 30px;
}

.hero-text-container {
  position: relative;
  width: 100%;
  max-width: 900px;
}

.hero-title {
  font-family: 'Monigue DEMO', sans-serif;
  font-size: clamp(48px, 8vw, 110px);
  font-weight: 400;
  line-height: 1.1;
  color: white;
  text-transform: uppercase;
  margin: 0;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
  letter-spacing: 2px;
}

.hero-subtitle {
  max-width: 600px;
  font-size: 16px;
  line-height: 1.6;
  color: #B3F90F;
  font-weight: 500;
  margin: 0;
}

.search-container {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}

.search-form {
  width: 100%;
  display: flex;
  gap: 12px;
  background: white;
  padding: 8px;
  border-radius: 50px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 24px;
  font-size: 15px;
  background: transparent;
  color: #333;
}

.search-input::placeholder {
  color: #999;
}

.search-button {
  background: #B3F90F;
  color: black;
  border: none;
  padding: 12px 32px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.search-button:hover {
  background: #a0e00d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(179, 249, 15, 0.4);
}

.location-button {
  background: transparent;
  color: #B3F90F;
  border: 2px solid #B3F90F;
  padding: 10px 24px;
  border-radius: 50px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.location-button:hover {
  background: rgba(179, 249, 15, 0.1);
}

.wave-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  z-index: 5;
}

.wave-decoration svg {
  display: block;
  width: 100%;
  height: auto;
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 16px 80px;
    min-height: 500px;
  }

  .search-form {
    flex-direction: column;
    border-radius: 24px;
  }

  .search-button {
    width: 100%;
  }
}
</style>
