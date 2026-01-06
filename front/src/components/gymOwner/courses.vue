<template>
  <div class="courses-page">
    <div class="main-page">
      <div class="top-section">
        <h1 class="courses-title">Gym Courses</h1>
        <button class="add-course-button" @click="showModal = true">Add Course</button>
      </div>

      <!-- THE MODAL -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal-box">
          <div class="modal-header">
            <h2>{{ isEditing ? "Edit course" : "Add course" }}</h2>
            <span
              class="close-btn"
              @click="
                showModal = false;
                isEditing = false;
                editingCourse = null;
              "
              >✕</span
            >
          </div>

          <div class="modal-body">
            <div class="row">
              <div class="field">
                <label>Course</label>
                <select v-model="course" :disabled="loading">
                  <option value="">Sélectionner un cours</option>
                  <option v-for="opt in courseOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>

              <div class="field">
                <label>Level</label>
                <select v-model="level" :disabled="loading">
                  <option value="">Sélectionner un niveau</option>
                  <option v-for="opt in levelOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row">
              <div class="field">
                <label class="tima">Time</label>
                <input type="number" v-model="time" />
              </div>

              <div class="field">
                <label>Unit</label>
                <select v-model="unit" :disabled="loading">
                  <option v-for="opt in unitOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
            </div>

            <div class="field full">
              <label>Description</label>
              <textarea v-model="description" :disabled="loading"></textarea>
            </div>
            
            <div v-if="error" class="error-message">{{ error }}</div>
          </div>

          <div class="modal-footer">
            <button class="add-btn" @click="addCourse" :disabled="loading">
              {{ loading ? "En cours..." : isEditing ? "Save" : "Add" }}
            </button>
          </div>
        </div>
      </div>
      <!-- END MODAL -->
      <!-- Error message -->
      <div v-if="error && !showModal" class="error-banner">{{ error }}</div>
      
      <!-- IF THERE ARE NO COURSES → SHOW EMPTY STATE -->
      <div v-if="courses.length === 0 && !loading" class="empty-picture">
        <img src="./empty.png" class="empty-image" />
        <h1 class="empty-text">Your page is empty</h1>
        <p class="add-courses-text">All added courses will be listed here</p>
      </div>
      
      <!-- Loading state -->
      <div v-if="loading && courses.length === 0" class="loading-state">
        <p>Chargement des cours...</p>
      </div>

      <!-- IF COURSES EXIST → SHOW CARDS -->
      <div v-else class="cards-grid">
        <div v-for="item in courses" :key="item.id" class="course-card">
          <div class="card-header">
            <h3 class="title">{{ item.title }}</h3>
            <span class="level-tag" :class="'level-' + item.level.toLowerCase().replace('_', '-')">
              {{ item.level_display || getLevelDisplay(item.level) }}
            </span>
            <span class="time-tag">
              <span class="clock">⏱</span>
              {{ item.time }}{{ item.unit === 'hour' ? 'h' : item.unit }}
            </span>
            <div class="menu-container">
              <div class="dots" @click="toggleMenu(item.id)">⋮</div>

              <div v-if="activeMenu === item.id" class="dropdown-menu">
                <div class="menu-item" @click="editCourse(item)">Edit</div>
                <div class="menu-item delete" @click="deleteCourse(item.id)">Delete</div>
              </div>
            </div>
          </div>

          <p class="desc">
            {{ item.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api.js";

const showModal = ref(false);
const loading = ref(false);
const error = ref("");

// Mapping des valeurs du backend vers l'affichage
const courseOptions = [
  { value: "yoga", label: "Yoga" },
  { value: "hiit_burn", label: "HIIT" },
  { value: "barbell_basics", label: "Strength" },
  { value: "indoor_cycling", label: "Indoor Cycling" },
  { value: "crossfit", label: "CrossFit" },
  { value: "pilates", label: "Pilates" },
];

const levelOptions = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "all_levels", label: "All levels" },
];

const unitOptions = [
  { value: "min", label: "min" },
  { value: "hour", label: "h" },
];

const course = ref("");
const level = ref("");
const time = ref("");
const unit = ref("min");
const description = ref("");
const courses = ref([]);
const activeMenu = ref(null);
const isEditing = ref(false);
const editingCourse = ref(null);
const props = defineProps({
  selectedGymId: {
    type: [Number, String],
    required: true,
  },
  triggerAddCourse: {
    type: Number,
    default: 0
  }
});

watch(
  () => props.triggerAddCourse,
  (newVal) => {
    if (newVal > 0) {
      showModal.value = true;
      isEditing.value = false;
      editingCourse.value = null;
      resetForm();
    }
  }
);

const loadCourses = async () => {
  if (!props.selectedGymId) return;

  loading.value = true;
  error.value = "";
  try {
    const response = await api.getCourses(props.selectedGymId);
    courses.value = response.data.map((c) => ({
      id: c.id,
      title: c.name_display || c.name,
      name: c.name, // Garder la valeur originale pour l'édition
      level: c.level,
      level_display: c.level_display,
      time: c.duration_value,
      unit: c.duration_unit,
      description: c.description,
    }));
  } catch (err) {
    error.value = err.response?.data?.message || "Erreur lors du chargement des cours";
    console.error("Error loading courses:", err);
  } finally {
    loading.value = false;
  }
};

// Watch for changes in selectedGymId
import { watch } from "vue";
watch(
  () => props.selectedGymId,
  (newId) => {
    if (newId) {
      loadCourses();
    }
  },
  { immediate: true }
);

const addCourse = async () => {
  if (!course.value || !level.value || !time.value || !description.value) {
    error.value = "Veuillez remplir tous les champs";
    return;
  }

  if (!props.selectedGymId) {
    error.value = "Aucune salle disponible";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const courseData = {
      name: course.value,
      level: level.value,
      duration_value: parseInt(time.value),
      duration_unit: unit.value,
      description: description.value,
    };

    if (isEditing.value && editingCourse.value) {
      // Update existing course
      await api.updateCourse(props.selectedGymId, editingCourse.value, courseData);
    } else {
      // Create new course
      await api.createCourse(props.selectedGymId, courseData);
    }

    showModal.value = false;
    resetForm();
    await loadCourses();
  } catch (err) {
    error.value = err.response?.data?.message || err.response?.data?.error || "Erreur lors de la sauvegarde";
    console.error("Error saving course:", err);
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  course.value = "";
  level.value = "";
  time.value = "";
  unit.value = "min";
  description.value = "";
  isEditing.value = false;
  editingCourse.value = null;
};

const toggleMenu = (id) => {
  activeMenu.value = activeMenu.value === id ? null : id;
};

const editCourse = (item) => {
  course.value = item.name || item.title;
  level.value = item.level;
  time.value = item.time.toString();
  unit.value = item.unit;
  description.value = item.description;
  isEditing.value = true;
  editingCourse.value = item.id;
  showModal.value = true;
  activeMenu.value = null;
  error.value = "";
};

const deleteCourse = async (id) => {
  if (!confirm("Êtes-vous sûr de vouloir supprimer ce cours ?")) {
    return;
  }

  if (!props.selectedGymId) return;

  loading.value = true;
  error.value = "";

  try {
    await api.deleteCourse(props.selectedGymId, id);
    await loadCourses();
    activeMenu.value = null;
  } catch (err) {
    error.value = err.response?.data?.message || "Erreur lors de la suppression";
    console.error("Error deleting course:", err);
  } finally {
    loading.value = false;
  }
};

const getLevelDisplay = (level) => {
  const option = levelOptions.find((opt) => opt.value === level);
  return option ? option.label : level;
};
</script>

<style scoped>
.courses-page {
  width: 100%;
  height: 100vh;
  background-color: #ffffff;
  font-family: "Inter", sans-serif;
}

/* ===== MAIN PAGE ===== */
.main-page {
  padding: 0px 10px;
}

/* TOP SECTION */
.top-section {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.courses-title {
  font-size: 22px;
  font-weight: 600;
  color: #242424;
}

/* ADD COURSE BUTTON */
.add-course-button {
  background-color: #b3f90f;
  border: none;
  padding: 12px 26px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s ease;
}

.add-course-button:hover {
  opacity: 0.9;
}

/* ===== EMPTY STATE IMAGE + TEXT ===== */
.empty-picture {
  margin-top: 60px;
  width: 100%;
  text-align: center;
}

.empty-image {
  width: 260px;
  opacity: 0.9;
}

.empty-text {
  font-size: 26px;
  font-weight: 700;
  color: #1f1f1f;
  margin-top: 20px;
}

.add-courses-text {
  font-size: 13px;
  color: #8a8a8a;
  margin-top: 8px;
}
/* ===== MODAL OVERLAY ===== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.25);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

/* ===== MODAL BOX ===== */
.modal-box {
  width: 650px;
  background: #ffffff;
  border-radius: 12px;
  padding: 20px 30px 30px;
  box-shadow: 0 4px 25px rgba(0, 0, 0, 0.15);
  animation: popup 0.25s ease;
}

@keyframes popup {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

/* HEADER */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 20px;
  font-weight: 600;
}

.close-btn {
  font-size: 22px;
  cursor: pointer;
  opacity: 0.6;
}
.close-btn:hover {
  opacity: 1;
}

/* BODY FIELDS */
.modal-body {
  margin-top: 20px;
}

.row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.field {
  width: 50%;
  display: flex;
  flex-direction: column;
}

.field.full {
  width: 95%;
}

label {
  font-size: 13px;
  margin-bottom: 5px;
  color: #606060;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d6d6d6;
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  background-color: #f9fbfc;
}

textarea {
  height: 150px;
  resize: none;
}

/* FOOTER */
.modal-footer {
  display: flex;
  justify-content: center;
  margin-top: 15px;
}

.add-btn {
  background: #b3f90f;
  padding: 12px 40px;
  margin-right: -550px;
  border-radius: 25px;
  border: none;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
}

.add-btn:hover {
  opacity: 0.9;
}
.time {
  margin-left: 19px;
}
/* ===== GRID ===== */
.cards-grid {
  margin-top: 30px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

/* ===== CARD ===== */
/* NEW CARD EXACTLY LIKE THE DESIGN */
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
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #1f1f1f;
  margin: 0;
}

.dots {
  font-size: 22px;
  cursor: pointer;
  opacity: 0.5;
  margin-left: auto;
}

.dots:hover {
  opacity: 1;
}

.menu-container {
  position: relative;
  margin-left: auto;
}

/* DROPDOWN MENU */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 5px;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 6px 0;
  min-width: 100px;
  z-index: 10;
}

.menu-item {
  padding: 10px 20px;
  font-size: 14px;
  cursor: pointer;
  color: #333;
  transition: 0.2s;
}

.menu-item:hover {
  background: #f5f5f5;
}

.menu-item.delete {
  color: #ff0000;
}

/* TAGS EXACTLY LIKE THE IMAGE */
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
  margin-top: 12px;
  font-size: 13px;
  line-height: 1.4;
  color: #626262;
}

.error-message {
  color: #c33;
  font-size: 13px;
  margin-top: 10px;
  padding: 8px;
  background: #fee;
  border-radius: 4px;
}

.error-banner {
  background: #fee;
  color: #c33;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.add-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

select:disabled,
textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.level-tag.level-all-levels {
  background: #f2e5ff;
  color: #a035ff;
}
</style>
