<template>
  <div class="form-card">
    
    <h3 class="form-title">Write a review</h3>

    <form @submit.prevent="handleSubmit" class="review-form">
      <!-- User Info -->
      <div class="user-info">
        <div>
          <!-- User name is now dynamic via prop -->
          <div class="user-name">{{ userName }}</div>
          <div class="user-status">Posted publicly</div>
        </div>
      </div>

      <!-- Global Rating -->
      <div class="form-group">
        <label class="form-label">Global rating</label>
        <!-- Using Font Awesome stars with proper filled/empty states -->
        <div class="star-rating">
          <button
            v-for="star in 5"
            :key="`global-${star}`"
            type="button"
            :class="['star-btn', { 'filled': form.overallRating >= star }]"
            @click="form.overallRating = star"
            aria-label="Rate"
          >
            <i :class="['fa-star', form.overallRating >= star ? 'fas' : 'far']"></i>
          </button>
        </div>
      </div>

      <!-- Divider -->
      <div class="form-divider">Or</div>

      <!-- Rating Categories -->
      <div class="form-group">
        <label class="form-label">Rating based on</label>
        <div class="categories-list">
          <!-- Each category has Font Awesome star ratings -->
          <div v-for="category in ratingCategories" :key="category" class="category-item">
            <span class="category-name">{{ capitalizeCategory(category) }}</span>
            <div class="category-stars">
              <button
                v-for="star in 5"
                :key="`${category}-${star}`"
                type="button"
                :class="['category-star-btn', { 'filled': form.ratings[category] >= star }]"
                @click="form.ratings[category] = star"
                aria-label="Rate"
              >
                <i :class="['fa-star', form.ratings[category] >= star ? 'fas' : 'far']"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Comment -->
      <div class="form-group">
        <textarea 
          v-model="form.comment"
          class="form-textarea"
          placeholder="Add a comment"
          rows="3"
        ></textarea>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="submit-btn" :disabled="submitting">
        {{ submitting ? 'sending..' : 'Submit' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, defineProps, defineEmits } from 'vue';
import api from '../api';

const props = defineProps({
  userName: {
    type: String,
    default: 'Anonymous User'
  },
  gymId: {
    type: [Number, String],
    required: true
  }
});

const emit = defineEmits(['review-submitted']);

const submitting = ref(false);
const ratingCategories = ['Cleanliness', 'Equipment', 'Staff', 'Value'];

const form = reactive({
  overallRating: 0,
  comment: '',
  ratings: {
    Cleanliness: 0,
    Equipment: 0,
    Staff: 0,
    Value: 0
  }
});

const capitalizeCategory = (category) => {
  return category;
};

const resetForm = () => {
  form.comment = '';
  form.overallRating = 0;
  form.ratings = {
    Cleanliness: 0,
    Equipment: 0,
    Staff: 0,
    Value: 0
  };
};

const handleSubmit = async () => {
  if (form.overallRating === 0 && form.comment === '') {
    alert('Please rate or add a comment');
    return;
  }

  try {
    submitting.value = true;
    
    // Payload mapping based on backend Avis model
    // note_globale is calculated by backend
    const payload = {
        commentaire: form.comment,
        // Mapping fields to backend expectations:
        note_proprete: form.ratings.Cleanliness || 0, 
        note_equipement: form.ratings.Equipment || 0,
        note_personnel: form.ratings.Staff || 0,
        note_rapport_qualite_prix: form.ratings.Value || 0
    };

    console.log('Submitting review payload:', payload);

    await api.addAvis(props.gymId, payload);
    
    resetForm();
    emit('review-submitted');
    alert('Review submitted successfully!');
  } catch (err) {
    console.error('Error submitting review:', err);
    alert('Error submitting review. Please ensure you are logged in as a Client.');
  } finally {
    submitting.value = false;
  }
};
</script>

<style scoped>
.form-card {
  border-radius: 8px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--surface-page, #FFF);
  padding: 24px;
  
  gap: 16px;

display: flex;
flex-direction: column;
}

.form-title {
  color: var(--text-headlines, #040B1A);
font-size: 20px;
font-style: normal;
font-weight: 600;
line-height: 120%; /* 24px */
}

.user-info {
  display: flex;
  flex-direction: row;

gap: 16px;

}

.user-name {
  color: var(--Text-Headings, #141414);
font-size: 14px;
font-style: normal;
font-weight: 500;
line-height: 20px; /* 142.857% */
}

.user-status {
 color: var(--light-dash, #65697A);
font-size: 12px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 166.667% */
}

.review-form {
  display: flex;
flex-direction: column;
align-items: flex-start;
gap: 24px;
align-self: stretch;
}

.form-group {
 display: flex;
flex-direction: column;
align-items: flex-start;
gap: 8px;
align-self: stretch;
}

.form-label {
  color: var(--Text-Headings, #141414);
font-size: 14px;
font-style: normal;
font-weight: 500;
line-height: 20px; /* 142.857% */
}

.star-rating {
  display: flex;
  gap: 8px;
  
}

.star-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #d1d5db;
  cursor: pointer;
  padding: 0;
  transition: all 0.2s;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.star-btn.filled {
  color: #053ecd;
}

.star-btn.filled i {
  color: #053ecd;
}

.star-btn i {
  font-size: 25px;
}

.star-btn:hover i {
  color: #053ecd;
}

.form-divider {
  color: var(--light-dash, #65697A);
font-size: 12px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 166.667% */
}

.categories-list {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
gap: 8px;
align-self: stretch;
}

.category-item {
  display: flex;
align-items: flex-start;
gap: 40px;
align-self: stretch;
}

.category-name {
  color: var(--text-headlines, #040B1A);
font-family: Inter;
font-size: 14px;
font-style: normal;
font-weight: 400;
line-height: 20px; /* 142.857% */
}

.category-stars {
  display: flex;
  gap: 2px;
}

.category-star-btn {
  background: none;
  border: none;
  font-size: 16px;
  color: #d1d5db;
  cursor: pointer;
  padding: 0;
  transition: all 0.2s;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.category-star-btn.filled {
  color: #053ecd;
}

.category-star-btn.filled i {
  color: #053ecd;
}

.category-star-btn i {
  font-size: 16px;
}

.category-star-btn:hover i {
  color: #053ecd;
}

.form-textarea {
  padding: 16px;
  
  border-radius: 320px;
  font-size: 12px;
  font-family: inherit;
  resize: vertical;
  
border: var(--Border-width-sm, 1px) solid var(--border-dash, #E8E7EC);
background: var(--bg-gray-dash, #F9FBFC);

  width: 100%;
    box-sizing: border-box;
    height: 50px;
    
    

}

.form-textarea:focus {
  outline: none;
  border-color: #053ecd;
  background: #f9fafb;
}

.submit-btn {
  background: #B3F90F;
  color: #000;
  border: none;
  padding: 12px 24px;
  border-radius: 24px;
  font-weight: 600;
  font-size: var(--Fontsize-Body-sm, 14px);
  cursor: pointer;
  transition: all 0.2s;
  line-height: var(--Line-height-Body-sm, 20px); /* 142.857% */
  width: fit-content;
  align-self: flex-end;
}

.submit-btn:hover:not(:disabled) {
  background: #a8d609;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
