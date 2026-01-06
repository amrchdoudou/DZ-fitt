<template>
  <div class="schedule-container">
    <div class="schedule-card">
      <div class="schedule-header">
        <h2 class="schedule-title">Gym Courses Schedule:</h2>
        <button class="add-button" @click="openAddModal">Add</button>
      </div>
      <div class="calendar-grid">
        <div class="day-column" v-for="day in days" :key="day">
          <div class="day-header">{{ day }}</div>
          <div class="day-content">
            <div
              v-for="course in getCoursesByDay(day)"
              :key="course.id"
              class="course-card"
              :style="{ borderLeftColor: getLevelColor(course.level) }"
              @click="openEditModal(course)"
            >
              <button class="delete-btn" @click.stop="deleteCourse(course.id)">×</button>
              <div class="course-time-block" :style="{ color: getLevelColor(course.level) }">
                <div class="time-line">{{ course.time.substring(0, 5) }}</div>
                <div class="time-line">{{ course.endTime ? course.endTime.substring(0, 5) : '...' }}</div>
              </div>
              <span class="course-name">{{ course.name }} - {{ course.level }}</span>
              <span class="course-room">{{ course.room }}</span>
              <span
                class="course-instructor"
                :style="{ color: getLevelColor(course.level) }"
                >{{ course.instructor }}</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Add/Edit -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <button class="close-btn" @click="closeModal">×</button>
        <h3 class="modal-title">Add Schedule</h3>

        <form @submit.prevent="saveCourse" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label>Day</label>
              <select v-model="formData.day">
                <option value="SUN">Sunday</option>
                <option value="MON">Monday</option>
                <option value="TUE">Tuesday</option>
                <option value="WED">Wednesday</option>
                <option value="THU">Thursday</option>
                <option value="FRI">Friday</option>
                <option value="SAT">Saturday</option>
              </select>
            </div>
            <div class="form-group">
              <label>Course</label>
              <select v-model="formData.courseId">
                <option
                  v-for="course in availableCourses"
                  :key="course.id"
                  :value="course.id"
                >
                  {{ course.displayName }} ({{ course.displayLevel }})
                </option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Start time</label>
              <select v-model="formData.time">
                <option value="08:00:00">8:00 am</option>
                <option value="09:00:00">9:00 am</option>
                <option value="10:00:00">10:00 am</option>
                <option value="11:00:00">11:00 am</option>
                <option value="12:00:00">12:00 pm</option>
                <option value="13:00:00">1:00 pm</option>
                <option value="14:00:00">2:00 pm</option>
                <option value="15:00:00">3:00 pm</option>
                <option value="16:00:00">4:00 pm</option>
                <option value="17:00:00">5:00 pm</option>
              </select>
            </div>
            <div class="form-group">
              <label>Finish time</label>
              <select v-model="formData.endTime">
                <option value="09:00:00">9:00 am</option>
                <option value="09:30:00">9:30 am</option>
                <option value="10:00:00">10:00 am</option>
                <option value="10:30:00">10:30 am</option>
                <option value="11:00:00">11:00 am</option>
                <option value="11:30:00">11:30 am</option>
                <option value="12:00:00">12:00 pm</option>
                <option value="12:30:00">12:30 pm</option>
                <option value="13:30:00">1:30 pm</option>
                <option value="14:30:00">2:30 pm</option>
                <option value="15:30:00">3:30 pm</option>
                <option value="16:30:00">4:30 pm</option>
                <option value="17:30:00">5:30 pm</option>
                <option value="18:30:00">6:30 pm</option>
              </select>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Room</label>
              <input type="text" v-model="formData.room" placeholder="room 2" />
            </div>
            <div class="form-group">
              <label>Coach</label>
              <input type="text" v-model="formData.instructor" placeholder="Rania" />
            </div>
          </div>

          <div class="modal-actions">
            <button
              v-if="isEditing"
              type="button"
              class="delete-modal-btn"
              @click="deleteAndClose"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="3,6 5,6 21,6"></polyline>
                <path
                  d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6m3,0V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2v2"
                ></path>
              </svg>
              Delete
            </button>
            <button type="submit" class="add-modal-btn">Add</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import api from "../../api";

const props = defineProps({
  selectedGymId: {
    type: [String, Number],
    required: true
  }
});

const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];

const levelColors = {
  Beginner: "#FF9500",
  Intermediate: "#AF52DE",
  Advanced: "#007AFF",
};

const getLevelColor = (level) => {
  return levelColors[level] || "#FF9500";
};

const availableCourses = ref([]);
const isLoading = ref(true);
const error = ref(null);

const fetchCourses = async () => {
  if (!props.selectedGymId) return;
  
  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.getCourses(props.selectedGymId);
    availableCourses.value = response.data.map(course => ({
      id: course.id,
      name: course.name, // choice field yoga, hiit_burn...
      displayName: course.name_display || course.name,
      level: course.level,
      displayLevel: course.level_display || course.level
    }));
    
    // Set default course in form if not set
    if (availableCourses.value.length > 0 && !formData.courseId) {
      formData.courseId = availableCourses.value[0].id;
    }
  } catch (err) {
    console.error('Error fetching courses:', err);
    error.value = 'Failed to load courses';
  } finally {
    isLoading.value = false;
  }
};

const selectedCourse = computed(() => {
  return availableCourses.value.find((c) => c.id === formData.courseId);
});

const selectedCourseLevels = computed(() => {
  // In the current backend, each Course object has exactly one level.
  // But the UI seems to expect multiple levels for a "Course Name".
  // Let's adapt: find all Courses with the same 'name' and list their levels.
  if (!selectedCourse.value) return ["Beginner", "Intermediate", "Advanced"];
  
  return availableCourses.value
    .filter(c => c.name === selectedCourse.value.name)
    .map(c => c.displayLevel);
});

const onCourseChange = () => {
  // No action needed for now, formData.courseId is already bound
};

const schedule = ref([]);

// Fetch schedules from API
const fetchSchedules = async () => {
  if (!props.selectedGymId) return;

  try {
    const response = await api.getSalleSchedules(props.selectedGymId);
    console.log('Fetched schedules raw data:', response.data);
    schedule.value = response.data.map(sched => ({
      id: sched.id,
      day: convertDayToAbbr(sched.day),
      time: sched.start_time,
      endTime: sched.end_time,
      name: sched.course_name || "Course",
      room: sched.room || "",
      instructor: sched.coach || "",
      level: sched.course_level || "Beginner",
      courseId: sched.course
    }));
    console.log('Mapped schedules:', schedule.value);
  } catch (err) {
    console.error('Error fetching schedules:', err);
  }
};

// Convert day name to abbreviation
const convertDayToAbbr = (day) => {
  if (!day) return 'SUN';
  const dayLower = day.toLowerCase();
  const dayMap = {
    'sunday': 'SUN', 'monday': 'MON', 'tuesday': 'TUE',
    'wednesday': 'WED', 'thursday': 'THU', 'friday': 'FRI', 'saturday': 'SAT'
  };
  return dayMap[dayLower] || day.substring(0, 3).toUpperCase();
};

// Convert abbreviation to full day name
const convertAbbrToDay = (abbr) => {
  const dayMap = {
    'SUN': 'sunday', 'MON': 'monday', 'TUE': 'tuesday',
    'WED': 'wednesday', 'THU': 'thursday', 'FRI': 'friday', 'SAT': 'saturday'
  };
  return dayMap[abbr] || abbr.toLowerCase();
};

// Watch for selectedGymId changes
watch(() => props.selectedGymId, () => {
  fetchCourses();
  fetchSchedules();
}, { immediate: true });

onMounted(() => {
  fetchCourses();
  fetchSchedules();
});

const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);

const formData = reactive({
  day: "SUN",
  time: "09:00:00",
  endTime: "10:00:00",
  courseId: null,
  room: "",
  instructor: "",
  level: "Beginner",
});

const getCoursesByDay = (day) => {
  return schedule.value.filter((course) => course.day === day);
};

const openAddModal = () => {
  isEditing.value = false;
  editingId.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (course) => {
  isEditing.value = true;
  editingId.value = course.id;
  formData.day = course.day;
  formData.time = course.time;
  formData.endTime = course.endTime;
  formData.courseId = course.courseId;
  formData.room = course.room;
  formData.instructor = course.instructor;
  formData.level = course.level;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const resetForm = () => {
  formData.day = "SUN";
  formData.time = "09:00:00";
  formData.endTime = "10:00:00";
  formData.courseId = availableCourses.value[0]?.id || null;
  formData.room = "";
  formData.instructor = "";
  formData.level = "Beginner";
};

const saveCourse = async () => {
  if (!props.selectedGymId) {
    console.error('❌ Cannot save: selectedGymId is missing');
    alert('Error: No gym selected.');
    return;
  }

  console.log('📝 Initializing save: formData.endTime =', formData.endTime);

  const scheduleData = {
    day: convertAbbrToDay(formData.day),
    start_time: formData.time,
    end_time: formData.endTime,
    course: formData.courseId,
    room: formData.room,
    coach: formData.instructor,
  };

  console.log('🚀 Sending scheduleData to API:', JSON.stringify(scheduleData, null, 2));
  
  try {
    if (isEditing.value) {
      await api.updateSchedule(props.selectedGymId, editingId.value, scheduleData);
    } else {
      await api.createSchedule(props.selectedGymId, scheduleData);
    }
    await fetchSchedules();
    closeModal();
  } catch (err) {
    console.error('Error saving schedule:', err);
    if (err.response && err.response.data) {
      console.log('Backend error details:', err.response.data);
      alert('Error: ' + JSON.stringify(err.response.data));
    } else {
      alert('Failed to save schedule. Please try again.');
    }
  }
};

const deleteCourse = async (id) => {
  if (!props.selectedGymId) return;

  try {
    await api.deleteSchedule(props.selectedGymId, id);
    await fetchSchedules();
  } catch (err) {
    console.error('Error deleting schedule:', err);
    alert('Failed to delete schedule. Please try again.');
  }
};

const deleteAndClose = () => {
  if (editingId.value) {
    deleteCourse(editingId.value);
  }
  closeModal();
};
</script>

<style scoped>
.schedule-container {
  width: 100%;
  display: flex;
  gap: 12px;
  padding: 0px;
  background-color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
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
  width: 100%;
  align-self: stretch;
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
  color: #040b1a;
  font-size: 24px;
  font-weight: 600;
  line-height: 20px;
  margin: 0;
  font-style: normal;
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
  display: flex;
  width: 100%;
  border-top: 1px solid #e8e8e8;
}

.day-column {
  flex: 1;
  border-right: 1px solid #e8e8e8;
  min-width: 120px;
}

.day-column:last-child {
  border-right: 1px solid #e8e8e8;
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
  min-height: 95px;
  flex-direction: column;
  align-items: flex-start;
  gap: 3px;
  border: 1px solid #e0e0e0;
  background: var(--white, #FFF);;

  flex-shrink: 0;
align-self: stretch;
}

.course-card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 6px;
  border-left: 3px solid;
  background: #fafafa;
  border-radius: 4px;
  width: 100%;
  max-width: 108px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  align-self: stretch;
}

.course-card:hover {
  background: #f0f0f0;
}

.course-card:hover .delete-btn {
  opacity: 1;
}

.delete-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  width: 18px;
  height: 18px;
  border: none;
  background: #ff4444;
  color: white;
  border-radius: 50%;
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-btn:hover {
  background: #cc0000;
}

.course-time {
  font-size: 11px;
  font-weight: 600;
}

.course-name {
  font-size: 12px;
  font-weight: 600;
  color: #040b1a;
}

.course-room {
  font-size: 10px;
  color: #65697a;
}

.course-instructor {
  font-size: 10px;
  font-weight: 500;
}

.course-level {
  font-size: 10px;
  font-weight: 500;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
  padding-left: 24px;
  padding-right: 24px;
  padding-top: 24px;
  padding-bottom: 0px;
  width: 634px;
  height: 540px;
  gap: 32px;
  position: absolute;
  display: flex;
  flex-direction: column;
}

.close-btn {
  position: absolute;
  top: 24px;
  right: 24px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #9ca3af;
  line-height: 1;
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #040b1a;
}

.modal-title {
  color: var(--text-headlines, #040b1a);
  font-size: 24px;
  font-style: normal;
  font-weight: 600;
  line-height: 20px; /* 83.333% */
  height: 0px;
  align-self: stretch;
  stroke-width: 1.3px;
  stroke: var(--border, #eee);
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  color: var(--light-dash, #65697a);

  /* Body/sm/Semibold */
  font-family: var(--Type-Font-family-Primary);
  font-size: var(--Fontsize-Body-sm, 14px);
  font-style: normal;
  font-weight: 600;
  line-height: var(--Line-height-Body-sm, 20px); /* 142.857% */
}

.form-group input,
.form-group select {
  display: flex;
  align-items: center;
  align-self: stretch;
  padding: 16px;
  gap: 8px;
  border: var(--Border-width-sm, 1px) solid var(--Border-Primary, #D6D6D6);
  border-radius: var(--Scale-100, 4px);
  flex: 1 0 0;
  font-size: var(--Fontsize-Body-md, 16px);
  color: var(--text-headlines, #040B1A);
  font-family: var(--Type-Font-family-Primary);
  font-style: normal;
  font-weight: 500;
  line-height: var(--Line-height-Body-md, 24px); /* 150% */
  background: var(--bg-gray-dash, #F9FBFC);
  outline: none;
  transition: border-color 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
}

.form-group select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%239CA3AF' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  padding-right: 36px;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #b3f90f;
}

.modal-actions {
  display: flex;
  gap: 8px;
  margin-top: 18px;
  margin-bottom: 0px;
  justify-content: flex-end;
}

.delete-modal-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 134px;
  height: 44px;
  padding: 12px 24px;
  background: white;
  border-radius: 24px;
  border: 1px solid #EA0101;
  color: #EA0101;
font-size: var(--Fontsize-Body-sm, 14px);
font-style: normal;
font-weight: 600;
line-height: var(--Line-height-Body-sm, 20px); /* 142.857% */
  cursor: pointer;
  transition: all 0.2s ease;
}

.delete-modal-btn:hover {
  background: #fef2f2;
}

.delete-modal-btn svg {
  stroke: #EA0101;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.add-modal-btn {
  display: flex;
width: 134px;
  padding: 12px 24px;
  justify-content: center;
align-items: center;
gap: 8px;
  border: none;
  background: #B3F90F;
  border-radius: 24px;
  color: #000;
font-size: var(--Fontsize-Body-sm, 14px);
font-style: normal;
font-weight: 600;
line-height: var(--Line-height-Body-sm, 20px); /* 142.857% */
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.add-modal-btn:hover {
  background: #a0e00d;
}
</style>
