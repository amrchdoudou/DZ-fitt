<template>
  <div class="layout">
    <SideBar 
      ref="sidebarRef"
      :activeNav="activePage" 
      @change-page="switchPage" 
      @add-gym="handleAddGym"
      @gym-selected="handleGymSelected"
      @trigger-add-course="handleTriggerAddCourse"
    />

    <div class="main-area">
      <!-- HEADER -->
      <TopHeader :name="userName" />

      <div class="content-area">
        <div class="gym-reviews-page">
          <!-- FontAwesome CDN -->
          <link 
            rel="stylesheet" 
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
          />
          
          <h1 class="page-title">Gym Reviews</h1>
          
          <!-- Loading State -->
          <div v-if="loading" class="loading">
            <i class="fas fa-spinner fa-spin"></i>
            Chargement des avis...
          </div>
          
          <!-- Error State -->
          <div v-else-if="error" class="error">
            <i class="fas fa-exclamation-circle"></i>
            {{ error }}
          </div>
          
          <!-- Empty State -->
          <div v-else-if="reviews.length === 0" class="empty-state">
            <div class="empty-icon">
               <img 
                src="../assets/empty-reviews.svg" 
                alt="No reviews yet" 
                class="empty-svg"
              />
            </div>
            <h2 class="empty-title">Your page is empty</h2>
            <p class="empty-description">All added reviews will be listed here</p>
          </div>
          
          <!-- Reviews Grid -->
          <div v-else class="reviews-grid">
            <div 
              v-for="review in reviews" 
              :key="review.id" 
              class="review-card"
            >
              <!-- Header -->
              <div class="review-header">
                <div class="user-info">
                  <span class="username">{{ review.username }}</span>
                  <span class="rating-text">{{ review.overallRating }}/5</span>
                  <i class="fas fa-star star-icon"></i>
                </div>
                <span class="date">{{ formatDate(review.date) }}</span>
              </div>
              
              <!-- Comment -->
              <p class="comment">{{ review.comment }}</p>
              
              <!-- Ratings -->
              <div class="ratings-grid">
                <div 
                  v-for="(value, key) in review.ratings" 
                  :key="key" 
                  class="rating-row"
                >
                  <span class="category">{{ key }}</span>
                  <div class="stars">
                    <i 
                      v-for="star in 5" 
                      :key="star"
                      :class="['fa-star', star <= value ? 'fas filled' : 'far empty']"
                    ></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import SideBar from "../components/gymOwner/sideBar.vue";
import TopHeader from "../components/gymOwner/top.vue";
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const router = useRouter();

// Sidebar & Header Logic
const activePage = ref("reviews");
const sidebarRef = ref(null);

const loadUserName = () => {
  try {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      return user.nom_complet || user.email || "Gym Owner";
    }
  } catch (e) {
    console.error("Error loading user data:", e);
  }
  return "Gym Owner";
};

const userName = ref(loadUserName());

const switchPage = (page) => {
  if (page === 'dashboard') router.push('/Dashboardm');
  else if (page === 'mygym') router.push('/MyGym');
  else if (page === 'schedule') router.push('/Schedule');
  else if (page === 'settings') {
    // Navigate to MyGym and then switch to setting tab
    router.push('/MyGym').then(() => {
      // Small delay to allow MyGym to load and then we can emit if needed 
      // but simpler is to just handle top-level routes here.
    });
  }
  else activePage.value = page;
};

const handleAddGym = () => {
  router.push('/MyGym');
};

const handleGymSelected = (gymId) => {
  localStorage.setItem('selectedGymId', gymId);
  fetchReviews();
};

const handleTriggerAddCourse = () => {
  router.push('/Schedule');
};

// Reviews State
const reviews = ref([]);
const loading = ref(true);
const error = ref(null);

const getCurrentSalleId = () => {
  try {
    const selectedGym = localStorage.getItem('selectedGymId');
    if (selectedGym) return selectedGym;
    
    const gymsStr = localStorage.getItem('myGyms');
    if (gymsStr) {
      const gyms = JSON.parse(gymsStr);
      if (gyms.length > 0) return gyms[0].id;
    }
  } catch (e) {
    console.error('Error getting salle ID:', e);
  }
  return null;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = date.getDate();
  const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];
  const month = months[date.getMonth()];
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
};

const transformReview = (backendReview) => {
  return {
    id: backendReview.id,
    username: backendReview.utilisateur?.nom_complet || backendReview.utilisateur?.email || 'Utilisateur',
    overallRating: backendReview.note_globale || 0,
    date: backendReview.date_publication || new Date().toISOString(),
    comment: backendReview.commentaire || '',
    ratings: {
      Cleanliness: backendReview.note_proprete || 0,
      Equipment: backendReview.note_equipement || 0,
      Staff: backendReview.note_personnel || 0,
      Price: backendReview.note_rapport_qualite_prix || 0
    }
  };
};

const fetchReviews = async () => {
  const salleId = getCurrentSalleId();
  if (!salleId) {
    loading.value = false;
    return;
  }

  try {
    loading.value = true;
    const response = await api.getSalleAvis(salleId);
    reviews.value = response.data.map(transformReview);
  } catch (err) {
    console.error('Error fetching reviews:', err);
    error.value = 'Erreur lors du chargement des avis';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchReviews();
});
</script>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
}

.main-area {
  margin-left: 275px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  width: calc(100% - 275px);
}

.content-area {
  flex: 1;
  overflow-y: auto;
  width: 100%;
  padding: 20px;
  background: #ffffff;
}

.gym-reviews-page {
  padding: 12px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-headlines, #040B1A);
  margin-bottom: 24px;
}

.loading, .error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #6b7280;
  font-size: 16px;
}

.error {
  color: #ef4444;
}

/* Reviews Grid */
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 1024px) {
  .reviews-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .reviews-grid {
    grid-template-columns: 1fr;
  }
}

.review-card {
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 200px;
}

.review-card:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
  transform: translateY(-2px);
}

.review-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.username {
  color: var(--text-headlines, #040b1a);
  font-size: 15px;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 70%;
}

.date {
  color: var(--light-dash, #9ca3af);
  font-size: 12px;
}

.rating-text {
  color: var(--light-dash, #9ca3af);
  font-size: 14px;
  font-weight: 700;
}

.star-icon {
  color: #053ecd;
  font-size: 14px;
}

.comment {
  color: #4b5563;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex-grow: 1;
}

.ratings-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  padding-top: 16px;
  border-top: 1px solid #f9fafb;
}

.rating-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  color: #6b7280;
  font-size: 13px;
  font-weight: 500;
}

.stars {
  display: flex;
  gap: 2px;
}

.stars .fa-star {
  font-size: 12px;
}

.stars .fa-star.filled {
  color: #053ecd;
}

.stars .fa-star.empty {
  color: #e5e7eb;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  gap: 16px;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
}

.empty-svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #9ca3af;
}
</style>