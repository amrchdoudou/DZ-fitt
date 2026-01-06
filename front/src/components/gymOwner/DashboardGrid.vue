<template>
  <div class="dashboard-container">
    <div class="dashboard-grid">
      <!-- Improve Your Gym Profile Card -->
      <div class="card improve-card">
        <div class="part1">
          <div class="card-header">
            <FontAwesomeIcon :icon="['fas', 'chart-line']" />
            <h2>{{ $i18n.t('management.improve_profile') }}</h2>
          </div>
          <p class="card-description">
            {{ $i18n.t('management.improve_desc') }}
          </p>
        </div>
        <div class="chart-container">
          <img src="../../assets/Group 320.svg" alt="Bar Chart" class="barchart-image" />
        </div>
      </div>

      <!-- Create Your First Class Card -->
      <div class="card create-card">
        <div class="part1">
        <div class="card-header">
          <FontAwesomeIcon :icon="['fab', 'dribbble']" />
          <h2>{{ $i18n.t('management.create_class') }}</h2>
        </div>
        <p class="card-description">{{ $i18n.t('management.create_desc') }}</p>
        </div>

        <div class="chart-container">
          <img src="../../assets/Frame 1632530506.svg" alt="Create Class" class="barchart-image" />
        </div>

        <!-- <img
          src="../assets/Frame 1632530506.svg"
          alt="Create Class"
          class="create-class-image"
        /> -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { i18n } from "../../i18n.js";

const $i18n = i18n;

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

// const chartData = ref([
//   { height: '40%' },
//   { height: '60%' },
//   { height: '45%' },
//   { height: '80%' },
//   { height: '55%' },
// ])
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.dashboard-container {
  /* margin-left moved to parent layout */
  padding: 0 32px; 
  background: #FAFAFA;
  
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  
}

.dashboard-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 10px;

  margin: 0 auto;
}

/* Card Styles */
.card {
  height: 179px;
  border-radius: 8px;
  border: 1px solid #e8e7ec;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  background: #ffffff;
  display: flex;
  align-items: flex-start;
  flex: 1 0 0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 8px;
  width: 100%;
}

/* Typography */
.card h2 {
  font-size: 16px;
  font-weight: 600;
  color:  var(--text-headlines, #040B1A);;
  margin: 0;
  line-height: 20px;
}

.card-description {
  font-size: 14px;
  font-weight: 400;
  font-style: normal;
  color: #6b7280;
  line-height: 20px;
  margin-top: 20px;
}

/* Icon styling */
.card-header svg {
  width: 20px;
  height: 20px;
  color: #6b7280;
  flex-shrink: 0;
}

/* Improve Card Specific */
.improve-card {
  grid-column: 1;
}

.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;

  align-self: center;
  margin-top: 0px;
  margin-right: auto;
  margin-bottom: 0px;
  margin-left: auto;
}

.barchart-image {
  height: 170px;
  width: 208px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: flex-start;
  height: 60px;
  gap: 6px;
}

.bar-wrapper {
  flex: 0 0 12px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  height: 100%;
}

/* Bar styling */
.bar {
  width: 100%;
  background: #2563eb;
  border-radius: 4px 4px 0 0;
  transition: all 0.2s ease;
}

.bar:hover {
  opacity: 0.85;
}

/* Create Card Specific */
.create-card {
  grid-column: 2;
  display: flex;

  background: #ffffff;
}

.create-class-image {
  margin-top: 0px;
  width: 208px;
  height: 201px;
  margin-top: 0px;
  margin-right: 0px;
  margin-left: auto;
  display: flex;
  flex-direction: column;
align-items: flex-start;
align-self: stretch;
}

/* Responsive Design */
@media (max-width: 900px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .improve-card,
  .create-card {
    grid-column: auto;
  }
}

@media (max-width: 640px) {
  .dashboard-container {
    padding: 16px;
    margin-left: 0;
  }

  .dashboard-grid {
    gap: 12px;
  }

  .card {
    padding: 16px;
    height: auto;
    min-height: 179px;
  }

  .card h2 {
    font-size: 15px;
  }

  .chart-container {
    margin-top: 12px;
  }
}
</style>
