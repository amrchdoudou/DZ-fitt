<template>
  <div class="reviews-container">
<!-- FontAwesome CDN -->
          <link 
            rel="stylesheet" 
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
          />

    <!-- Top Navigation Tabs -->
    <!-- <TabsNavigation 
      :activeTab="activeTab"
      @update:activeTab="activeTab = $event"
    /> -->

    <!-- Main Content Area -->
    <!-- <div class="main-content" v-if="activeTab === 'Reviews'"> -->
    <div class="main-content" >
      <!-- Left Section: Reviews List -->
      <div class="reviews-column">
        <ReviewsList 
          :reviews="reviews"
          :loading="loading"
          :error="error"
        />
      </div>

      <!-- Right Section: Stats & Form -->
      <div class="sidebar-column">
        <ReviewsStats :reviews="reviews" />
        <ReviewForm :gymId="props.gymId" :userName="props.userName" @review-submitted="fetchReviews" />
      </div>
    </div>

    <!-- Other Tabs -->
    <!-- <div v-else class="other-content">
      <p>{{ activeTab }} content coming soon...</p>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps, watch } from 'vue';
import ReviewsList from './ReviewsList.vue';
import ReviewForm from './ReviewForm.vue';
import ReviewsStats from './ReviewsStats.vue';
import api from '../api';

const props = defineProps({
  gymId: {
    type: [Number, String],
    required: true
  },
  reviews: {
    type: Array,
    default: () => []
  },
  userName: {
    type: String,
    default: 'Anonymous User'
  }
});

const reviews = ref([]);
const loading = ref(false);
const error = ref(null);

// Initialize from props
onMounted(() => {
  if (props.reviews) {
    reviews.value = props.reviews;
  }
});

// Watch for prop changes
watch(() => props.reviews, (newReviews) => {
  if (newReviews) {
    reviews.value = newReviews;
  }
});

// Keep fetch for re-loading after submission
const fetchReviews = async () => {
  if (!props.gymId) return;
  
  try {
    loading.value = true;
    const response = await api.getSalleAvis(props.gymId);
    reviews.value = response.data;
  } catch (err) {
    console.error('Error loading reviews:', err);
    error.value = 'Error loading reviews';
  } finally {
    loading.value = false;
  }
};

watch(() => props.gymId, (newId) => {
  // If ID changes, we rely on parent to pass new reviews prop usually, 
  // but if we want to be safe we can clear or fetch. 
  // Since parent handles data fetching for the page, props should update.
});
</script>

<style scoped>
.reviews-container {
  
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #f9fafb;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
  gap: 12px;
  padding: 0px;
  background: #ffffff;

}

.reviews-column {
  flex: 1;
  overflow-y: auto;
  padding-right: 0px;
  min-width: 0;
}

.sidebar-column {
  
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding-right: 0px;
}

.other-content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
  color: #6b7280;
  font-size: 18px;
}

/* Scrollbar styling */
.reviews-column::-webkit-scrollbar,
.sidebar-column::-webkit-scrollbar {
  width: 6px;
}

.reviews-column::-webkit-scrollbar-track,
.sidebar-column::-webkit-scrollbar-track {
  background: transparent;
}

.reviews-column::-webkit-scrollbar-thumb,
.sidebar-column::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.reviews-column::-webkit-scrollbar-thumb:hover,
.sidebar-column::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}
</style>
