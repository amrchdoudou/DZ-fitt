<template>
  <div class="stats-container">
    <div class="stat-card">
      <span class="stat-label">Total Profile Views</span>
      <span class="stat-value">0</span>
      <span class="stat-period">last month</span>
    </div>
    
    <div class="stat-card">
      <span class="stat-label">Average rating</span>
      <span class="stat-value">no rating yet</span>
      <span class="stat-period">last month</span>
    </div>
    
    <div class="stat-card">
      <span class="stat-label">Courses Published</span>
      <span class="stat-value">0</span>
      <span class="stat-period">last month</span>
    </div>
    
  </div>
</template>

<script setup>
</script>

<style scoped>
.stats-container {
  width: 100%;

  display: flex;
  gap: 12px;
  padding: 0px;
  background-color: #FFFFFF;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.stat-card {
  display: flex;
  flex-direction: column;
  background-color: var(--bg-gray-dash, #F9FBFC);;
  border-radius: 12px;
  padding-left: 24px;
  padding-right: 24px;
  padding-top: 24px;
  padding-bottom: 0px;
  width: 100%;
  min-width: 200px;
  height: 161px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #F0F0F0;
  gap: 31px;
}

.stat-label {
  color: var(--light-dash, #65697A);
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 20px; /* 125% */
}

.stat-value {
  color: var(--text-headlines, #040B1A);
  font-style: normal;
  font-size: 24px;
  font-weight: 600;
  line-height: 20px; /* 83.333% */
}

.stat-period {
  color: var(--light-dash, #65697A);
  font-size: 16px;
  font-style: normal;
  font-weight: 500;
  line-height: 20px; /* 125% */
}
</style>