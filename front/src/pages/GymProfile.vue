<template>
  <div class="gym-profile">
    <Header />
    <div class="profile-container">
      <div v-if="loading" class="loading">Chargement du profil...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else class="profile-content">
        <div class="profile-header">
           <div class="gym-logo-container">
              <img v-if="gym.logo" :src="gym.logo" :alt="gym.nom" class="gym-logo-img" @error="handleImageError">
              <div v-else class="logo-placeholder">{{ gym.nom?.charAt(0) || 'G' }}</div>
           </div>
          <div class="header-info">
            <h1>{{ gym.nom }}</h1>
            <p class="address">📍 {{ gym.adresse }}, {{ gym.ville }}, {{ gym.wilaya }}</p>
            <div class="quick-stats">
              <span class="rating">⭐ {{ gym.note_moyenne ? Number(gym.note_moyenne).toFixed(1) : 'N/A' }}</span>
              <span class="price">💰 {{ gym.prix_moyen || 'Non spécifié' }}</span>
            </div>
          </div>
        </div>

        <div class="profile-body">
          <section class="description">
            <h2>À propos</h2>
            <p>{{ gym.description || 'Aucune description disponible.' }}</p>
          </section>

          <section class="services">
            <h2>Services</h2>
            <ul v-if="gym.services && gym.services.length">
              <li v-for="s in gym.services" :key="s.id">{{ s.service_nom }}</li>
            </ul>
            <p v-else>Aucun service répertorié.</p>
          </section>

          <section class="equipment">
            <h2>Équipements</h2>
            <ul v-if="gym.equipes && gym.equipes.length">
              <li v-for="e in gym.equipes" :key="e.id">{{ e.equipement_nom }}</li>
            </ul>
            <p v-else>Aucun équipement répertorié.</p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '../components/layouts/Header.vue';
import api from '../api';

export default {
  name: 'GymProfile',
  components: {
    Header
  },
  data() {
    return {
      gym: {},
      loading: true,
      error: null
    }
  },
  methods: {
    handleImageError(e) {
      // If image fails to load, replace with placeholder
      // This logic is a bit tricky with v-if/v-else, so we'll just hide the img and show a fallback if possible
      // But simpler: just unset the logo so v-else kicks in (if reactive) or style it.
      // Easiest is to set gym.logo to null.
      this.gym.logo = null;
    }
  },
  async mounted() {
    const id = this.$route.params.id;
    try {
      const response = await api.getPublicGym(id);
      this.gym = response.data;
    } catch (err) {
      console.error("Error fetching gym profile:", err);
      this.error = "Impossible de charger le profil de la salle.";
    } finally {
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.gym-profile {
  min-height: 100vh;
  background: #f5f7f9;
}

.profile-container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 20px;
}

.profile-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  padding: 40px;
}

.profile-header {
  display: flex;
  gap: 30px;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 30px;
  margin-bottom: 30px;
}

.gym-logo-container {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  overflow: hidden;
  flex-shrink: 0;
}

.gym-logo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  background: #0940BE;
  color: white;
  font-size: 48px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-info h1 {
  font-size: 32px;
  color: #333;
  margin-bottom: 8px;
}

.address {
  color: #666;
  font-size: 16px;
  margin-bottom: 12px;
}

.quick-stats {
  display: flex;
  gap: 20px;
  font-weight: 600;
}

.profile-body h2 {
  font-size: 22px;
  color: #0940BE;
  margin: 24px 0 12px;
}

.profile-body p {
  line-height: 1.6;
  color: #444;
}

ul {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  list-style: none;
  padding: 0;
}

li {
  background: #eef2ff;
  color: #0940BE;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}
</style>
