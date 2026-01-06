<template>
  <div class="courses-container">
    <div v-if="courses && courses.length === 0" class="no-courses">No courses available</div>
    <div v-else class="cards-grid">
      <div v-for="course in courses" :key="course.id" class="course-card">
        <div class="card-header">
          <h3 class="title">{{ course.nom }}</h3>
          <span class="level-tag" :class="'level-' + (course.level ? course.level.toLowerCase().replace('_', '-') : 'all-levels')">
            {{ course.level || 'All levels' }}
          </span>
          <span class="time-tag">
            <span class="clock">⏱</span>
            {{ course.duration }}
          </span>
        </div>
        <p class="desc">{{ course.description }}</p>
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
  courses: {
    type: Array,
    default: () => []
  }
});
</script>

<style scoped>
.courses-container {
  padding: 20px;
  background: white;
  min-height: 200px;
}

.no-courses {
  text-align: center;
  color: #666;
  padding: 40px;
}

/* ===== GRID ===== */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}

/* ===== CARD ===== */
.course-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 18px 20px;
  box-shadow: 0px 1px 3px rgba(0, 0, 0, 0.08);
  border: 1px solid #e8e7ec;
  transition: 0.2s ease;
}

.course-card:hover {
  transform: translateY(-2px);
}

/* CARD HEADER */
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #1f1f1f;
  margin: 0;
  margin-right: auto;
}

/* TAGS */
.level-tag {
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
}

.level-tag.level-beginner {
  background: #fff4e5;
  color: #c4580a;
}

.level-tag.level-intermediate {
  background: #e5f0ff;
  color: #0039c8;
}

.level-tag.level-advanced {
  background: #f2e5ff;
  color: #a035ff;
}

.level-tag.level-all-levels,
.level-tag.level-all {
  background: #f2e5ff;
  color: #a035ff;
}

.time-tag {
  background: #ffe8f4;
  color: #ff3ca6;
  font-size: 11px;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.clock {
  font-size: 13px;
  margin-right: 4px;
}

/* DESCRIPTION TEXT */
.desc {
  font-size: 13px;
  line-height: 1.4;
  color: #626262;
  margin: 0;
}
</style>
