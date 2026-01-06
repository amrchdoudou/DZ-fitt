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
        <DashboardGrid />
        
        <div class="dashboard-page">
          <StatsemptyDashboard />
          <CoursesSchadule />
          <ERecentReviews />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SideBar from "../components/gymOwner/sideBar.vue";
import TopHeader from "../components/gymOwner/top.vue";

import DashboardGrid from "../components/gymOwner/DashboardGrid.vue";
import StatsemptyDashboard from "../components/gymOwner/StatsemptyDashboard.vue";
import CoursesSchadule from "../components/gymOwner/CoursesSchadule.vue";

import ERecentReviews from '../components/gymOwner/ERecentReviews.vue';

export default {
  components: {
   SideBar,
   TopHeader,
    DashboardGrid,
    StatsemptyDashboard,
    CoursesSchadule,
    ERecentReviews
  },
  setup() {
    const router = useRouter();
    const activePage = ref("dashboard");
    const userName = ref("");

    onMounted(() => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        userName.value = user.full_name || user.nom_complet || user.email || "Gym Owner";
      }
    });

    const switchPage = (page) => {
      if (page === 'mygym') router.push('/MyGym');
      else if (page === 'reviews') router.push('/ReviewsPage');
      else if (page === 'schedule') router.push('/Schedule');
    };

    const handleAddGym = () => router.push('/MyGym');
    const handleGymSelected = (id) => {
      localStorage.setItem('selectedGymId', id);
      window.location.reload(); 
    };
    const handleTriggerAddCourse = () => router.push('/Schedule');

    return {
      activePage,
      userName,
      switchPage,
      handleAddGym,
      handleGymSelected,
      handleTriggerAddCourse
    };
  }
};
</script>

<style scoped>
.dashboard-page {
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  align-self: stretch;
  background: #FFF;
}
</style>
