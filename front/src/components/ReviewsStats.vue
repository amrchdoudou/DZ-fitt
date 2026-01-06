<template>
  <div class="stats-card">
    <h3 class="stats-title">About reviews</h3>
    
    <!-- Overall Rating -->
    <div class="overall-rating-section">
      <div class="row">
      <div class="rating-stars-large">
        <i v-for="star in 5" :key="star" class="fas fa-star"></i>
      </div>
      <div class="rating-number">{{ averageRating }}</div>
      <div class="rating-meta">out of 5</div>
      </div>
      <div class="total-reviews-count">{{ totalReviews }} global rating</div>
    </div>

    <!-- Rating Distribution Bars -->
    <div class="distribution-section">
      <div v-for="stars in [5, 4, 3, 2, 1]" :key="stars" class="distribution-item">
        <span class="percentage">{{ getPercentage(stars) }}%</span>
        <div class="bar-container">
          <div 
            class="bar-fill" 
            :style="{ width: getPercentage(stars) + '%' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  reviews: {
    type: Array,
    required: true
  }
});

const totalReviews = computed(() => props.reviews.length);

const averageRating = computed(() => {
  if (props.reviews.length === 0) return '0.0';
  const sum = props.reviews.reduce((acc, review) => acc + (review.note_globale || 0), 0);
  return (sum / props.reviews.length).toFixed(1);
});

const getRatingCount = (stars) => {
  return props.reviews.filter(review => 
    Math.round(review.note_globale || 0) === stars
  ).length;
};

const getPercentage = (stars) => {
  if (totalReviews.value === 0) return 0;
  const count = getRatingCount(stars);
  return Math.round((count / totalReviews.value) * 100);
};
</script>

<style scoped>
.stats-card {
  border-radius: 8px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--surface-page, #FFF);
  padding: 24px;
  gap: 16px;

  display: flex;
flex-direction: column;
}

.stats-title {
  color: var(--text-headlines, #040B1A);
font-size: 20px;
font-style: normal;
font-weight: 600;
line-height: 120%; /* 24px */
}

.overall-rating-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;

  
}

.row{
  display: flex;
  align-items: flex-end;
  gap: 4px;
}

.rating-stars-large {
  display: flex;
  gap: 2px;
  
}

.rating-stars-large i {
  font-size: 25px;
  color: #053ecd;
}

.rating-number {
  color: var(--Text-Headings, #141414);
font-size: 14px;
font-style: normal;
font-weight: 500;
line-height: 20px; /* 142.857% */
}

.rating-meta {
  color: var(--Text-Headings, #141414);
font-size: 14px;
font-style: normal;
font-weight: 500;
line-height: 20px; /* 142.857% */
}

.total-reviews-count {
  color: var(--light-dash, #65697A);
font-family: var(--Type-Font-family-Primary, Inter);
font-size: 12px;
font-style: normal;
font-weight: 400;
line-height: var(--Line-height-Body-md, 24px); /* 200% */
}

.distribution-section {
  display: flex;
  flex-direction: column;
gap: 4px;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}

.percentage {
  color: var(--light-dash, #65697A);

font-size: 10px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 200% */
}

.bar-container {
 display: flex;
width: 262px;
height: 7px;
padding-right: 35px;
align-items: center;
flex-shrink: 0;
border-radius: 32px;
border: 0.5px solid var(--border-dash, #E8E7EC);
background: #FAFAFF;
}

.bar-fill {
  height: 100%;
  border-radius: 32px;
  background: #053ecd;
  transition: width 0.3s ease;
}
</style>
