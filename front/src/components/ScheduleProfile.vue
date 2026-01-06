<template>
  <div class="schedule-container">
    <h2 class="schedule-title">Courses scheduled this week</h2>

    <div class="calendar-grid">
      <div
        class="day-column"
        v-for="day in days"
        :key="day"
      >
        <div class="day-header">
          {{ dayNames[day] }}
        </div>

        <div class="day-content">
          <div
            v-for="course in getCoursesByDay(day)"
            :key="course.id"
            class="course-card"
            :style="{ borderLeftColor: getLevelColor(course.level) }"
          >
            <div class="course-time">
              {{ course.time }} - {{ course.endTime }}
            </div>
            <div class="course-name">{{ course.name }}</div>
            <div class="course-room">{{ course.room }}</div>
            <div class="course-instructor">{{ course.instructor }}</div>
          </div>

          <!-- pqs de cours-->
          <div
            v-if="getCoursesByDay(day).length === 0"
            class="empty-day"
          >

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

/* jours */
const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

const dayNames = {
  SUN: "Sun",
  MON: "Mon",
  TUE: "Tue",
  WED: "Wed",
  THU: "Thu",
  FRI: "Fri",
  SAT: "Sat",
};

/* les couleurs des niveau*/
const levelColors = {
  Beginner: "#FF9500",
  Intermediate: "#AF52DE",
  Advanced: "#007AFF",
};

const getLevelColor = (level) => levelColors[level] || "#FF9500";

const props = defineProps({
  gymId: {
    type: [Number, String],
    required: true
  },
  schedules: {
    type: Array,
    default: () => []
  }
});

const getCoursesByDay = (day) => {
  // schedule items from backend (via ProfilPage) already look like:
  // { id, day_of_week: 'monday', start_time, end_time, course_name, room, instructor_name }
  // We need to map them to the format expected by template:
  // { id, day, time, endTime, name, room, instructor }
  
  if (!props.schedules) return [];

  const dayMapping = {
    'sunday': 'SUN',
    'monday': 'MON',
    'tuesday': 'TUE',
    'wednesday': 'WED',
    'thursday': 'THU',
    'friday': 'FRI',
    'saturday': 'SAT'
  };

  return props.schedules
    .filter(item => {
      const mappedDay = dayMapping[item.day_of_week?.toLowerCase()] || item.day_of_week;
      return mappedDay === day;
    })
    .map(item => ({
      id: item.id,
      day: dayMapping[item.day_of_week?.toLowerCase()] || item.day_of_week,
      time: item.start_time?.substring(0, 5),
      endTime: item.end_time?.substring(0, 5),
      name: item.course_name,
      room: item.room,
      instructor: item.instructor_name
    }));
};
</script>

<style scoped>
.schedule-container {
  
  font-family: Arial, sans-serif;

  display: flex;
padding: 24px 32px;
flex-direction: column;
align-items: flex-start;
gap: 16px;
align-self: stretch;
border-radius: 8px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--surface-page, #FFF);
}

.schedule-title {
  color: var(--text-headlines, #040B1A);
font-family: Inter;
font-size: 20px;
font-style: normal;
font-weight: 600;
line-height: 120%; /* 24px */
}

.calendar-grid {
  display: flex;
padding: 0 0px;
align-items: flex-start;
gap: 0px;
align-self: stretch;

border: 1px solid #e0e0e0;

margin: 0px 16px;

}

.day-column {
  flex: 1;
display: flex;

  border-left: 1px solid #e0e0e0;
  border-right: 1px solid #e0e0e0;

 flex-direction: column;     

}

.day-header {
  display: flex;
padding: 16px 8px;
flex-direction: column;
align-items: flex-start;
flex: 1 0 0;
border-radius: 0 4px 0 0;
border: 1px  solid #E0E0E0;
background: #FFF;
}

.day-content {
  padding: 0px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.course-card {
  padding: 6px;
  border-left: 4px solid;
  background: #ffffff;
  font-size: 11px;
  border-radius: 4px;
}

.course-time {
  font-weight: bold;
}

.course-name {
  margin-top: 2px;
}

.course-room,
.course-instructor {
  color: #666;
}

.empty-day {
    flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ccc;
  font-size: 12px;
  border: 0px solid #e0e0e0;

}
</style>
