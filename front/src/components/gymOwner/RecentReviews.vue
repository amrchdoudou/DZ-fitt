<template>
  <!-- <div class="recent-reviews-section"> -->
    <!-- FontAwesome CDN -->
    <link 
      rel="stylesheet" 
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    />
    <div class="recent-reviews">
   <div class="reviewsRecentmm">
    <div class="header">
      <h2 class="title">Recent reviews</h2>
      <a href="#" @click.prevent="goToAllReviews" class="view-all-link">View all</a>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i>
      Loading reviews...
    </div>

    <!-- Empty State -->
    <div v-else-if="reviews.length === 0" class="empty-state">
       <div class="empty-icon">
          <img src="../../assets/empty-reviews.svg" alt="No reviews yet" class="empty-svg" />
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
        @click="goToReviews(review.id)"
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
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../api';

const props = defineProps({
  selectedGymId: {
    type: [String, Number],
    required: true
  },
  limit: {
    type: Number,
    default: 3
  }
});

const router = useRouter();

const emit = defineEmits(['view-all']);

const reviews = ref([]);
const loading = ref(false);

const formatDate = (dateString) => {
  const date = new Date(dateString);
  const day = date.getDate();
  const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];
  const month = months[date.getMonth()];
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
};

// ajouter pour naviguer vers la page des avis
const goToAllReviews = () => {
  router.push("/ReviewsPage");
};

const goToReviews = (reviewId) => {
  // router.push(`/ReviewsPage/${reviewId}`)
  router.push(`/ReviewsPage`);
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

const loadReviews = async () => {
  if (!props.selectedGymId) return;

  loading.value = true;
  
  try {
    const response = await api.getSalleAvis(props.selectedGymId);
    const allReviews = response.data.map(transformReview);
    reviews.value = allReviews.slice(0, props.limit);
  } catch (err) {
    console.error('Error loading reviews:', err);
    reviews.value = [];
  } finally {
    loading.value = false;
  }
};

watch(
  () => props.selectedGymId,
  (newId) => {
    if (newId) {
      loadReviews();
    }
  },
  { immediate: true }
);

onMounted(() => {
  loadReviews();
});
</script>

<style scoped>
.recent-reviews {
  width: 100%;
  display: flex;

  padding: 0px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.reviewsRecentmm {
  width: 100%;
  /* Removed fixed height constraint to allow content to flow naturally */
  min-height: 320px; 
  display: flex;
  padding: 24px 16px;
  flex-direction: column;
  gap: 24px;
  align-self: stretch;
  border-radius: 12px;
  border: 1px solid var(--border-dash, #e8e7ec);
  background: var(--bg-gray-dash, #f9fbfc);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.header {
  padding: 0 8px; /* Reduced vertical padding since parent handles it */
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.title {
  font-size: 20px; /* Slightly smaller for better hierarchy */
  font-weight: 600;
  color: var(--text-headlines, #040b1a);
  margin: 0;
  line-height: 24px;
}

.view-all-link {
  color: var(--Color, #0039c8);
  font-size: 14px;
  font-weight: 600;
  line-height: 20px;
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
}

.view-all-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #6b7280;
  font-size: 14px;
}


.reviews-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px; /* Increased gap for breathing room */
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
  padding: 20px; /* Increased padding */
  display: flex;
  flex-direction: column;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 200px; /* Ensure uniform height look */
}

.review-card:hover {
  border-color: #2563eb;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
  transform: translateY(-2px);
}

.review-header {
  display: flex;
  flex-direction: column; /* Stacked header for better organization */
  gap: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  justify-content: space-between; /* Spread name and date */
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

.rating-badge {
  display: flex;
  align-items: center;
  gap: 4px;
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
  -webkit-line-clamp: 3; /* Limit text lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex-grow: 1; /* Pushes ratings to bottom */
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
  font-size: 12px; /* Smaller stars for sub-ratings */
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
  padding: 60px 24px;
  text-align: center;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 4px;
}

.empty-description {
  font-size: 14px;
  color: #9ca3af;
}
</style>