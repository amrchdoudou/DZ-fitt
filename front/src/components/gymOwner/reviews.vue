<template>
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
    <div v-else-if="reviews.length === 0" class="empty-picture">
      <img 
        src="./empty.png" 
        alt="No reviews yet" 
        class="empty-image"
      />
      <h1 class="empty-text">Your page is empty</h1>
      <p class="add-courses-text">All added reviews will be listed here</p>
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
</template>

<script setup>
import { ref, watch } from 'vue'
import api from '../../api'

// Props - exactly like Courses
const props = defineProps({
  selectedGymId: {
    type: [String, Number],
    required: true
  }
})

// State
const reviews = ref([])
const loading = ref(false)
const error = ref('')

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const day = date.getDate()
  const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
  const month = months[date.getMonth()]
  const year = date.getFullYear()
  return `${day} ${month} ${year}`
}

// Transform backend review data to component format
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
  }
}

// Load reviews - exactly like loadCourses in Courses component
const loadReviews = async () => {
  if (!props.selectedGymId) return

  loading.value = true
  error.value = ''
  
  try {
    const response = await api.getSalleAvis(props.selectedGymId)
    reviews.value = response.data.map(transformReview)
  } catch (err) {
    error.value = err.response?.data?.message || 'Erreur lors du chargement des avis'
    console.error('Error loading reviews:', err)
  } finally {
    loading.value = false
  }
}

// Watch for changes in selectedGymId - exactly like Courses
watch(
  () => props.selectedGymId,
  (newId) => {
    if (newId) {
      loadReviews()
    }
  },
  { immediate: true }  // Load on mount, just like Courses
)
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.gym-reviews-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #ffffff;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
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

/* Empty State */
.empty-picture {
  margin-top: 60px;
  width: 100%;
  text-align: center;
}

.empty-image {
  width: 260px;
  opacity: 0.9;
}

.empty-text {
  font-size: 26px;
  font-weight: 700;
  color: #1f1f1f;
  margin-top: 20px;
}

.add-courses-text {
  font-size: 13px;
  color: #8a8a8a;
  margin-top: 8px;
}

/* Reviews Grid */
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

@media (max-width: 900px) {
  .reviews-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .reviews-grid {
    grid-template-columns: 1fr;
  }
}

.review-card {
  background: #FFF;
  border-radius: 12px;
  border: 1px solid #F0F0F0;
  padding: 20px;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-weight: 600;
  color: #1a1a2e;
  font-size: 15px;
}

.rating-text {
  color: #6b7280;
  font-size: 14px;
}

.star-icon {
  color: #053ECD;
  font-size: 14px;
}

.date {
  color: #9ca3af;
  font-size: 13px;
}

.comment {
  color: #374151;
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.5;
}

.ratings-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rating-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.category {
  color: #6b7280;
  font-size: 13px;
}

.stars {
  display: flex;
  gap: 2px;
}

.stars .fa-star {
  font-size: 14px;
}

.stars .fa-star.filled {
  color: #053ECD;
}

.stars .fa-star.empty {
  color: #d1d5db;
}
</style>
