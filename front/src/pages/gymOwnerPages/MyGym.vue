<template>
  <div class="layout">

    <SideBar 
      ref="sidebarRef"
      :activeNav="activePage" 
      @change-page="switchPage" 
      @add-gym="handleAddGym"
      @gym-selected="handleGymSelected"
      @trigger-add-course="handleTriggerAddCourse"
    />

    <div class="main-area">

      <!-- HEADER -->
      <TopHeader :name="userName" />

      <div class="content-area">
        <component 
          :is="currentComponent"
          @updateName="updateName"
          @gymSaved="handleGymSaved"
          :selectedGymId="selectedGymId"
          :triggerAddCourse="triggerAddCounter"
          :key="componentKey"
          ref="currentComponentRef"
        />
      </div>

    </div>

  </div>
</template>

<script>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"

// Components
import SideBar from "../../components/gymOwner/sideBar.vue"
import TopHeader from "../../components/gymOwner/top.vue"

// Pages
import Courses from "../../components/gymOwner/courses.vue"
import Settings from "../../components/gymOwner/settings.vue"
import Profile from "../../components/gymOwner/profile.vue"
import Dashboard from "../../components/gymOwner/DashboardGrid.vue"
import Reviews from "../../components/gymOwner/reviews.vue"

export default {
  components: { SideBar, TopHeader },

  setup() {
    const router = useRouter()
    const activePage = ref("mygym")
    const componentKey = ref(0)
    const currentComponentRef = ref(null)
    const sidebarRef = ref(null)
    const storedGymId = localStorage.getItem('selectedGymId');
    const selectedGymId = ref(storedGymId && storedGymId !== 'null' ? storedGymId : null) 

    // Charger le nom de l'utilisateur depuis localStorage
    const loadUserName = () => {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          return user.full_name || user.email || "Gym Owner";
        }
      } catch (e) {
        console.error("Error loading user data:", e);
      }
      return "Gym Owner";
    };

    // اسم المالك المعروض في الهيدر
    const userName = ref(loadUserName())

    const updateName = (newName) => {
      userName.value = newName
    }

    const switchPage = (page) => {
      if (page === 'dashboard') {
        router.push('/Dashboardm');
      } else if (page === 'reviews') {
        router.push('/ReviewsPage');
      } else {
        activePage.value = page;
        // Force component refresh for internal tabs
        componentKey.value++;
      }
    };

    const handleAddGym = () => {
      // Switch to profile page and trigger create mode
      activePage.value = "mygym"
      selectedGymId.value = 'new' // Set to 'new' to trigger create mode in Profile
      componentKey.value++
    }
    
    const handleGymSelected = (gymId) => {
      // Update selected gym when user picks from dropdown
      console.log("🎯 MyGym: Gym selected event received", gymId);
      
      selectedGymId.value = gymId;
      localStorage.setItem('selectedGymId', gymId);
      
      componentKey.value++; // Refresh component with new gym ID
    }
    
    const triggerAddCounter = ref(0)
    
    const handleTriggerAddCourse = () => {
      // Must be on courses page
      if (activePage.value !== "courses") {
        activePage.value = "courses"
        componentKey.value++
      }
      // Increment counter to trigger watcher in Courses
      setTimeout(() => {
        triggerAddCounter.value++
      }, 100)
    }

    const handleGymSaved = async (newGymId) => {
      console.log("💾 MyGym: Gym saved event received", newGymId);
      // Refresh the sidebar gym list after a gym is saved
      if (sidebarRef.value && sidebarRef.value.loadGyms) {
        // Force refresh labels
        await sidebarRef.value.loadGyms(false); 
      }
      
      // If a new gym was created, select it
      if (newGymId) {
        selectedGymId.value = newGymId;
        localStorage.setItem('selectedGymId', newGymId);
        
        // Give sidebar a tiny bit of time to reload the list, then select the right label
        setTimeout(() => {
          if (sidebarRef.value && sidebarRef.value.loadGyms) {
            sidebarRef.value.loadGyms(false);
          }
        }, 500);
      }
      
      componentKey.value++;
    }

    const currentComponent = computed(() => {
      const pages = {
        dashboard: Dashboard,
        mygym: Profile,
        reviews: Reviews,
        courses: Courses,
        settings: Settings,
      }
      return pages[activePage.value] || Profile
    })

    return { 
      activePage, 
      switchPage, 
      currentComponent, 
      userName, 
      updateName, 
      handleAddGym,
      handleGymSaved,
      handleGymSelected,
      selectedGymId,
      componentKey,
      currentComponentRef,
      sidebarRef,
      triggerAddCounter,
      handleTriggerAddCourse
    }
  },
}
</script>

<style>
  * {
  font-family: 'Inter', sans-serif;
}
.layout {
  display: flex;
  height: 100vh; /* full viewport height */
}

/* Sidebar assumed to be 280px wide */
.sidebar {
  width: 280px;
  flex-shrink: 0; /* prevent shrinking */
  height: 100vh;
  position: fixed; /* sidebar stays fixed */
  top: 0;
  left: 0;
  background: #fff; /* sidebar background */
  box-shadow: 2px 0 5px rgba(0,0,0,0.1);
  z-index: 10;
}

/* Main area next to sidebar */
.main-area {
  margin-left: 280px; /* leave space for sidebar */
  display: flex;
  flex-direction: column;
  height: 100vh;
  
  overflow: hidden;
  width: calc(100% - 280px);
}

/* Top header fixed height */
.main-area > .top-header {
  flex-shrink: 0;
  width: 100%;
}

/* Content fills remaining space under header */
.content-area {
  flex: 1; /* fill remaining vertical space */
  overflow-y: auto; /* scroll if content is long */
  width: 100%;
  padding: 20px; /* optional */
  box-sizing: border-box;
}


</style>
