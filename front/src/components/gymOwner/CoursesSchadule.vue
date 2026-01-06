<template>
  <div class="schedule-container">
    <div class="schedule-card">
      <div class="schedule-header">
        <h2 class="schedule-title">Gym Courses Schadule:</h2>
        <button class="add-button">Add</button>
      </div>
      <div class="calendar-grid">
        <div class="day-column" v-for="day in days" :key="day">
          <div class="day-header">{{ day }}</div>
          <div class="day-content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
</script>

<style scoped>
.schedule-container {
  width: 100%;
  
   display: flex;
  gap: 12px;
  padding: 0px;
  background-color: #FFFFFF;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.schedule-card {
  border-radius: 12px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--bg-gray-dash, #F9FBFC);
  display: flex;
padding: 24px 16px;
flex-direction: column;
align-items: flex-start;
gap: 24px;
align-self: stretch;
width: 100%;

}

.schedule-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
  padding: 0px 16px;
  
}

.schedule-title {
  width: 740px;
  height: 20px;
  color: var(--text-headlines, #040B1A);
font-size: 24px;
font-style: normal;
font-weight: 600;
line-height: 20px; /* 83.333% */
}

.add-button {
 display: flex;
  background-color: #b3f90f;
  color: #000000;
  border: none;
  border-radius: 24px;
  padding: 12px 24px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  width: 92px;
  height: 44px;
  font-size: var(--Fontsize-Body-sm, 14px);
  line-height: var(--Line-height-Body-sm, 20px);
  font-weight: 600;
  font-style: normal;
}

.add-button:hover {
  background-color: #a0e00d;
}

.calendar-grid {
  width: 100%;
  display: flex;
  border-top: 1px solid #e8e8e8;
}

.day-column {
  flex: 1;
  border-right: 1px solid #e8e8e8;
  min-width: 120px;
}

.day-column:last-child {
  border-right: none;
}

.day-header {
  display: flex;
  padding: 16px 8px;
  flex-direction: column;
  align-items: flex-start;
  border-radius: 0 4px 0 0;
  border: 1px solid #e0e0e0;
  background: #fff;
  color: #65697a;
  font-size: 10px;
  font-weight: 700;
  line-height: 12px;
  font-style: normal;
}

.day-content {
  padding: 2px;
  display: flex;
  min-height: 78px;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  border: 1px solid #e0e0e0;
  background: var(--white, #FFF);;

  flex-shrink: 0;
align-self: stretch;
}
</style>
