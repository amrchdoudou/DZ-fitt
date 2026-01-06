<template>
  <div class="sidebar">
    <!-- Logo at the very top -->
    <div class="logo-container">
      <img src="./logo.svg" alt="Logo" class="logo" />
    </div>

    <!-- Header -->
    <div class="sidebar-header">
      <div class="gym-selector">
        <div class="gym-info">
          <p class="gym-label">{{ $i18n.t('management.gym_label') }}</p>
          <p class="gym-name">{{ selectedGym }}</p>
        </div>

        <button class="expand-btn" @click="toggleGymDropdown">
          <svg
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="none"
            :style="{ transform: isGymDropdownOpen ? 'rotate(180deg)' : 'rotate(0deg)' }"
          >
            <path
              d="M4 6L8 10L12 6"
              stroke="#999"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Gym Dropdown -->
    <div v-if="isGymDropdownOpen" class="gym-dropdown">
      <div
        v-for="gym in gyms"
        :key="gym.id"
        :class="['gym-option', { selected: selectedGym === gym.name }]"
        @click="selectGym(gym)"
      >
        <span class="gym-name-text">{{ gym.name }}</span>
        <button v-if="gym.id !== 'new'" class="delete-gym-btn" @click.stop="confirmDeleteGym(gym)">
          <img src="./trash.svg" class="nav-icon-small delete-icon" />
        </button>
      </div>

      <button class="gym-option add-gym" @click="addNewGym">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
          <path
            d="M8 3V13M3 8H13"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
        </svg>
        {{ $i18n.t('management.add_gym') }}
      </button>
    </div>

    <!-- NAVIGATION -->
    <nav class="nav-links">
      <div
        :class="['nav-item', { active: activeNav === 'dashboard' }]"
        @click="handleNav('dashboard')"
      >
        <img src="./chart.svg" class="nav-icon" />
        <span>{{ $i18n.t('management.dashboard') }}</span>
      </div>

      <div
        :class="['nav-item', { active: activeNav === 'mygym' }]"
        @click="handleNav('mygym')"
      >
        <img src="./user-edit.svg" class="nav-icon" />
        <span>{{ $i18n.t('management.my_gym') }}</span>
      </div>

      <div
        :class="['nav-item', { active: activeNav === 'reviews' }]"
        @click="handleNav('reviews')"
      >
        <img src="./star.svg" class="nav-icon" />
        <span>{{ $i18n.t('management.reviews') }}</span>
      </div>

      <div
        :class="['nav-item', { active: activeNav === 'courses' }]"
        @click="handleNav('courses')"
      >
        <img src="./dribbble.svg" class="nav-icon" />
        <span>{{ $i18n.t('management.courses') }}</span>

        <button class="add-icon" @click.stop="addCourse">
          <img src="./plus.svg" class="nav-icon" style="width: 16px; height: 16px;" />
        </button>
      </div>

      <div
        :class="['nav-item', { active: activeNav === 'settings' }]"
        @click="handleNav('settings')"
      >
        <img src="./setting.svg" class="nav-icon" />
        <span>{{ $i18n.t('management.settings') }}</span>
      </div>
    </nav>

    <!-- LOGOUT FIXED AT BOTTOM -->
    <div class="logout-container">
      <button class="logout-btn" @click="logout">
        <img src="./logout.svg" alt="Logout" class="logout-icon" />
        <span>{{ $i18n.t('navbar.logout') }}</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, defineProps, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import api from "../../api.js";
import { i18n } from "../../i18n.js";

const $i18n = i18n;

const emit = defineEmits(["change-page", "add-gym", "gym-selected"]);
const props = defineProps({ activeNav: String });

const router = useRouter();

const isGymDropdownOpen = ref(false);
const selectedGym = ref("");
const gyms = ref([]);

// Load gyms from backend
const loadGyms = async (emitSelection = false) => {
  try {
    console.log("🔄 Sidebar: Loading gyms...");
    const response = await api.getMySalles();
    gyms.value = response.data.map(salle => ({
      id: salle.id,
      name: salle.nom
    }));
    
    console.log("📋 Sidebar: Gyms loaded:", gyms.value);
    
    if (gyms.value.length > 0) {
      // Find what should be selected
      const storedId = localStorage.getItem('selectedGymId');
      const currentGym = gyms.value.find(g => String(g.id) === String(storedId)) || gyms.value[0];
      
      selectedGym.value = currentGym.name;
      
      // Only emit gym-selected on initial load or if explicitly requested
      if (emitSelection) {
        console.log("✅ Sidebar: Emitting gym-selected:", currentGym.id);
        emit("gym-selected", currentGym.id);
      }
    } else {
      console.log("⚠️ Sidebar: No gyms found");
    }
  } catch (error) {
    console.error("❌ Sidebar: Error loading gyms:", error);
  }
};

onMounted(async () => {
  console.log("🚀 Sidebar: Component mounted");
  await loadGyms(true); // Emit selection only on initial mount
});

// Watch for external changes in localStorage (optional helper)
// Or just let parent trigger loadGyms

const toggleGymDropdown = () => {
  isGymDropdownOpen.value = !isGymDropdownOpen.value;
  if (isGymDropdownOpen.value) {
    loadGyms(false); // Refresh list without emitting selection
  }
};

const selectGym = (gym) => {
  selectedGym.value = typeof gym === 'string' ? gym : gym.name;
  isGymDropdownOpen.value = false;
  
  // Emit the selected gym ID to parent
  if (typeof gym === 'object' && gym.id) {
    emit("gym-selected", gym.id);
  }
};

const addNewGym = () => {
  // Add "Untitled" gym to the list temporarily
  const untitledGym = {
    id: 'new',
    name: 'Untitled'
  };
  
  // Add to beginning of list if not already there
  if (!gyms.value.find(g => g.id === 'new')) {
    gyms.value.unshift(untitledGym);
  }
  
  // Select the untitled gym
  selectedGym.value = 'Untitled';
  isGymDropdownOpen.value = false;
  
  // Emit event to parent to handle gym creation
  emit("add-gym");
};

const confirmDeleteGym = async (gym) => {
  if (confirm(`Are you sure you want to delete "${gym.name}"? This action cannot be undone.`)) {
    try {
      if (gym.id !== 'new') {
        await api.deleteSalle(gym.id);
      }
      // Reload gyms
      await loadGyms(false);
      
      // If deleted gym was selected, select the first one or untitled
      if (selectedGym.value === gym.name) {
        if (gyms.value.length > 0) {
          selectGym(gyms.value[0]);
        } else {
          selectedGym.value = "";
          emit("gym-selected", null);
        }
      }
    } catch (error) {
      console.error("Error deleting gym:", error);
      alert("Failed to delete gym. Please try again.");
    }
  }
};

// Expose loadGyms so parent can refresh after save
defineExpose({ loadGyms });

const addCourse = () => {
  emit("change-page", "courses");
  // Small delay to ensure page switch, then trigger add modal
  setTimeout(() => emit("trigger-add-course"), 100);
};

const handleNav = (page) => emit("change-page", page);

// Enhanced logout function - clears all auth data and navigates to login
const logout = () => {
  // Clear all authentication tokens and user data
  localStorage.removeItem("authToken");
  localStorage.removeItem("userToken");
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  localStorage.removeItem("profil");

  // Optional: Clear all localStorage if needed
  // localStorage.clear();

  // Navigate to login page
  router.replace("/login");
};
</script>

<style scoped>
.sidebar {
  width: 280px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e8e7ec;
  display: flex;
  flex-direction: column;
  padding: 0;
  position: fixed;
  left: 0;
  top: 0;
}

/* LOGO AT THE TOP */
.logo-container {
  padding: 24px 20px 20px 20px;
  display: flex;
  justify-content: center;
}

.logo {
  width: 120px;
  height: auto;
}

/* SIDEBAR HEADER */
.sidebar-header {
  padding: 0 20px 20px 20px;
  margin-bottom: 12px;
}

.gym-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 12px 14px;
}

.gym-info {
  flex: 1;
}

.gym-label {
  font-size: 11px;
  color: #999;
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 500;
}

.gym-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin: 4px 0 0 0;
}

.expand-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.5;
  transition: 0.2s;
}

.expand-btn:hover {
  opacity: 1;
}

/* GYM DROPDOWN */
.gym-dropdown {
  margin: 0 20px 20px 20px;
  background: #f9fafb;
  border: 1px solid #e8e7ec;
  border-radius: 8px;
  padding: 4px;
  animation: slideDown 0.2s ease;
}
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.gym-option {
  width: 100%;
  padding: 10px 12px;
  background: none;
  border: none;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
  justify-content: space-between; /* Align name and delete button */
}
.gym-option .gym-name-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.gym-option .delete-gym-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px;
  opacity: 0;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  margin-left: 8px;
}
.gym-option:hover .delete-gym-btn {
  opacity: 0.7;
}
.gym-option .delete-gym-btn:hover {
  opacity: 1;
  background-color: #fee2e2;
  transform: scale(1.05);
}
.delete-icon {
  width: 16px;
  height: 16px;
}
.gym-option:hover {
  background: #ffffff;
  color: #1a1a1a;
}
.gym-option.selected {
  background: #2563eb;
  color: #ffffff;
}
.gym-option.add-gym {
  color: #2563eb;
  margin-top: 4px;
  border-top: 1px solid #e8e7ec;
  padding-top: 12px;
}
.gym-option.add-gym:hover {
  background: #edf5ff;
}

/* NAV LINKS */
.nav-links {
  flex: 1;
  padding: 0 12px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  margin-bottom: 4px;
  border-radius: 8px;
  text-decoration: none;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  transition: 0.2s;
  position: relative;
  cursor: pointer;
}
.nav-item:hover {
  background: #f5f5f5;
  color: #1a1a1a;
}
.nav-item.active {
  background: #edf5ff;
  color: #2563eb;
}
.nav-item.active .nav-icon {
  filter: brightness(0) saturate(100%) invert(37%) sepia(98%) saturate(1784%)
    hue-rotate(207deg) brightness(96%) contrast(92%);
}
.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
.nav-item span {
  flex: 1;
}
.add-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  transition: 0.2s;
  margin-left: auto;
}
.add-icon:hover {
  color: #1a1a1a;
}

/* LOGOUT FIXED AT BOTTOM */
.logout-container {
  margin-top: auto;
  padding: 0 12px 20px 12px;
}
.logout-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 28px;
  border: none;
  background: none;
  color: #ef4444;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: 0.2s;
  width: 100%;
}
.logout-btn:hover {
  background: #fef2f2;
}
.logout-btn svg {
  flex-shrink: 0;
}
.logout-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
</style>
