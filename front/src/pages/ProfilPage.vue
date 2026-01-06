<template>
  <div class="profil-page">
    <Header />
    <div v-if="loading" style="text-align:center; padding: 40px;">Chargement...</div>
    <div v-else-if="error" style="text-align:center; padding: 40px; color: red;">{{ error }}</div>
    <div v-else>
      <ProductCard :gym="gym" />
      <div class="space">
        <GymInfo :gym="gym" />
        <div class="spacer">
          <!-- Tabs -->
          <TabsNavigation v-model:activeTab="activeTab" />

          <ReviewsProfile v-if="activeTab === 'Reviews'" :reviews="gym.avis" :gymId="gym.id" :userName="user ? user.name : 'Anonymous User'" />
          <ScheduleProfile v-if="activeTab === 'Schedule'" :schedules="gym.schedules" :gymId="gym.id"/>

          <GalerieProfile v-if="activeTab === 'Galerie'" :photos="gym.photos_galerie" :gymId="gym.id"/>
          <CoursesProfile v-if="activeTab === 'Courses'" :courses="gym.courses" :gymId="gym.id"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "../components/layouts/Header.vue"
import ProductCard from "../components/ProductCard.vue";
import GymInfo from "../components/GymInfo.vue";
import TabsNavigation from "../components/TabsNavigation.vue";
import ReviewsProfile from "../components/ReviewsProfile.vue";
import ScheduleProfile from "../components/ScheduleProfile.vue";
import GalerieProfile from "../components/GalerieProfile.vue";
import CoursesProfile from "../components/CoursesProfile.vue";
import api from '../api';

export default {
  components: {
    Header,
    ProductCard,
    GymInfo,
    TabsNavigation,
    ReviewsProfile,
    ScheduleProfile,
    GalerieProfile,
    CoursesProfile,
  },

  data() {
    return {
      activeTab: 'Reviews',
      gym: null,
      loading: true,
      error: null,
      user: null
    };
  },

  async mounted() {
    this.checkUser(); // Check for logged in user immediately
    const id = this.$route.params.id;
    try {
      const response = await api.getPublicGym(id);
      this.gym = response.data;
    } catch (err) {
      console.error("Error fetching gym profile:", err);
      this.error = "Impossible de charger le profil.";
    } finally {
      this.loading = false;
    }
  },

  methods: {
    checkUser() {
      const userStr = localStorage.getItem('user');
      const profilStr = localStorage.getItem('profil'); // Try to get client profile if available
      
      if (userStr) {
        try {
          const userData = JSON.parse(userStr);
          let fullName = userData.full_name || userData.nom_complet || userData.username || 'User';
          
          if (profilStr) {
             const profilData = JSON.parse(profilStr);
             // Prefer profile name if available
             if (profilData.nom_complet) fullName = profilData.nom_complet;
             else if (profilData.nom && profilData.prenom) fullName = `${profilData.prenom} ${profilData.nom}`;
          }
          
          this.user = {
            name: fullName,
            ...userData
          };
        } catch (e) {
          console.error("Error parsing user data", e);
        }
      }
    }
  }
}
</script>
<style scoped>
.profil-page {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 34px;
  padding: 0px;
  background: var(--surface-page, #F9F9FB);
 
}
  
.space {
  display: grid;
  grid-template-columns: 350px 1fr; /* Fixed width for GymInfo (sidebar) to give it "more space" visual weight, or adjust ratio */
  gap: 24px; /* Increased gap for better spacing */
  align-items: start; 
  padding: 0px 8px; /* Consider increasing padding if page feels cramped */
  width: 100%;
  max-width: 1200px; /* Constrain max width for better readability on large screens */
  margin: 0 auto;
}

.spacer {
  display: flex;
  flex-direction: column; /* محتوى التابس عمودي */
  gap: 16px;
  padding: 24px 32px;
  border-radius: 8px;
  border: 1px solid var(--border-dash, #E8E7EC);
  background: var(--surface-page, #FFF);

  
}

</style>