<template>
  <div class="reviews-list-section">
    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <p>chargement...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p>{{ error }}</p>
    </div>

    <!-- Reviews List -->
    <div v-else class="reviews-list">
      <div 
        v-for="review in reviews" 
        :key="review.id" 
        class="review-card"
      >
        <div class="review-header">
          <div class="user-info">
             <span class="username">
              {{ getReviewerName(review) }}
            </span>
            <div class="rating-badge">
              <span class="rating-value">{{ review.note_globale ? Number(review.note_globale).toFixed(1) : 'N/A' }}</span>
              <i class="fas fa-star star-icon"></i>
            </div>
          </div>
          <span class="review-date">{{ formatDate(review.date_publication) }}</span>
        </div>

        <!-- Review Comment -->
        <!-- Corrected: Accessing comment field -->
        <p class="review-comment">{{ review.commentaire }}</p>

        <!-- Review Ratings -->
        <div class="review-ratings">
          <!-- Manually mapping the detailed ratings as they are separate fields in backend -->
          <div class="rating-row">
             <span class="category-label">Cleanliness</span>
             <div class="rating-stars">
               <i v-for="star in 5" :key="'prop'+star" :class="['fa-star', star <= review.note_proprete ? 'fas' : 'far']"></i>
             </div>
          </div>
          <div class="rating-row">
             <span class="category-label">Equipment</span>
             <div class="rating-stars">
               <i v-for="star in 5" :key="'equip'+star" :class="['fa-star', star <= review.note_equipement ? 'fas' : 'far']"></i>
             </div>
          </div>
          <div class="rating-row">
             <span class="category-label">Staff</span>
             <div class="rating-stars">
               <i v-for="star in 5" :key="'staff'+star" :class="['fa-star', star <= review.note_personnel ? 'fas' : 'far']"></i>
             </div>
          </div>
          <div class="rating-row">
             <span class="category-label">Value</span>
             <div class="rating-stars">
               <i v-for="star in 5" :key="'val'+star" :class="['fa-star', star <= review.note_rapport_qualite_prix ? 'fas' : 'far']"></i>
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, onMounted } from 'vue';

const props = defineProps({
  reviews: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  }
});

const getReviewerName = (review) => {
  if (review.utilisateur) {
    if (review.utilisateur.nom_complet && review.utilisateur.nom_complet.trim() !== '') {
        return review.utilisateur.nom_complet;
    }
    if (review.utilisateur.email) {
        return review.utilisateur.email;
    }
  }
  return 'Client'; // Fallback if no user data found
};

const capitalizeCategory = (category) => {
  const map = {
    cleanliness: 'Cleanliness',
    equipment: 'Equipment',
    staff: 'Staff',
    price: 'Price'
  };
  return map[category] || category;
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = String(date.getDate()).padStart(2, '0');
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const month = months[date.getMonth()];
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
};
</script>

<style scoped>
.reviews-list-section {
  flex: 1;
  overflow-y: auto;
  padding-right: 0px;
  
  
}

.loading-state,
.error-state {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 12px;

  
  min-width: 473px;
 
}

.review-card {
  
  border-radius: 12px;
border: 1px solid var(--border-dash, #E8E7EC);
background: #FFF;
  display: flex;
padding: 12px 18px;
flex-direction: column;
align-self: stretch;
gap: 16px;

  transition: all 0.2s;
}

.review-card:hover {
  border-color: #053ecd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-header {

  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  color: var(--text-headlines, #040B1A);
font-size: 16px;
font-style: normal;
font-weight: 600;
line-height: 24px; /* 150% */
}

.rating-badge {
  display: flex;
  align-items: center;
  gap: 4px;
  
}

.rating-value {
  color: var(--light-dash, #65697A);
font-size: 16px;
font-style: normal;
font-weight: 500;
line-height: 20px; /* 125% */
}

.star-icon {
  color: #053ecd;
border-color: #0034B6;

  display: flex;
width: 18px;
height: 18px;
justify-content: center;
align-items: center;
aspect-ratio: 1/1;
}

.review-date {
  color: var(--light-dash, #65697A);
font-size: 14px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 142.857% */
}

.review-comment {
  color: var(--text-headlines, #040B1A);

font-size: 16px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 125% */
}
.review-ratings {
  display: flex;
  flex-direction: column;
  gap: 8px;
 
}

.rating-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.category-label {
  color: var(--text-headlines, #040B1A);
font-size: 14px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 142.857% */
}

.rating-stars {
  display: flex;
  gap: 0px;
}

.rating-stars i {
  
  color: #053ecd;
  width: 18px;
height: 18px;
flex-shrink: 0;
}

.rating-stars i.far {
  color: #e5e7eb;
}

/* Scrollbar styling */
.reviews-list-section::-webkit-scrollbar {
  width: 6px;
}

.reviews-list-section::-webkit-scrollbar-track {
  background: transparent;
}

.reviews-list-section::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.reviews-list-section::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
