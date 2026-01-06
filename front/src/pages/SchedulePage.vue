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
        <div class="schedule-page-content">
          <GymSchadule :selectedGymId="selectedGymId" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";
import SideBar from "../components/gymOwner/sideBar.vue";
import TopHeader from "../components/gymOwner/top.vue";
import GymSchadule from "../components/gymOwner/GymSchadule.vue";

export default {
  components: {
    SideBar,
    TopHeader,
    GymSchadule,
  },
  setup() {
    const router = useRouter();
    const activePage = ref("schedule");
    const userName = ref("");
    const selectedGymId = ref(localStorage.getItem('selectedGymId') || null);

    const loadData = async () => {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          userName.value = user.full_name || user.nom_complet || user.email || "Gym Owner";
        }

        if (!selectedGymId.value) {
          const response = await api.getMySalles();
          if (response.data && response.data.length > 0) {
            selectedGymId.value = response.data[0].id;
          }
        }
      } catch (err) {
        console.error("Error loading data:", err);
      }
    };

    const switchPage = (page) => {
      if (page === 'dashboard') router.push('/Dashboardm');
      else if (page === 'mygym') router.push('/MyGym');
      else if (page === 'reviews') router.push('/ReviewsPage');
      else activePage.value = page;
    };

    const handleAddGym = () => router.push('/MyGym');
    const handleGymSelected = (id) => {
      selectedGymId.value = id;
      localStorage.setItem('selectedGymId', id);
    };
    const handleTriggerAddCourse = () => {
      // Logic for adding course if needed
    };

    onMounted(loadData);

    return {
      activePage,
      userName,
      selectedGymId,
      switchPage,
      handleAddGym,
      handleGymSelected,
      handleTriggerAddCourse
    };
  }
}
</script>

<style scoped>
.schedule-page-content {
  padding: 24px;
}
</style>
