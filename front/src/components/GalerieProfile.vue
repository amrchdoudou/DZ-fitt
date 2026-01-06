<template>
  <div class="galerie-container">
    <div v-if="photos && photos.length === 0" class="no-photos">No photos available</div>
    <div v-else class="photos-grid">
      <div v-for="photo in photos" :key="photo.id" class="photo-item">
        <img :src="photo.image" :alt="photo.caption || 'Gym Photo'" @click="openLightbox(photo)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  gymId: {
    type: [Number, String],
    required: true
  },
  photos: {
    type: Array,
    default: () => []
  }
});

const openLightbox = (photo) => {
  // Simple lightbox or just view implementation could go here
  window.open(photo.image, '_blank');
};
</script>

<style scoped>
.galerie-container {
  padding: 20px;
  background: white;
  border-radius: 8px;
  min-height: 200px;
}

.loading, .no-photos {
  text-align: center;
  color: #666;
  padding: 40px;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.photo-item {
  aspect-ratio: 16/9;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.photo-item:hover {
  transform: scale(1.02);
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
