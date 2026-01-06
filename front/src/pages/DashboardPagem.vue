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
        <DashboardGrid :selectedGymId="selectedGymId" />
        
        <div class="dashboard-page">
          <StatsDashboard :selectedGymId="selectedGymId" />
          <GymSchadule :selectedGymId="selectedGymId" />
          <RecentReviews 
            :selectedGymId="selectedGymId" 
            :limit="3"
            @view-all="handleViewAllReviews"
          />
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
import StatsDashboard from "../components/gymOwner/StatsDashboard.vue";
import GymSchadule from "../components/gymOwner/GymSchadule.vue";
import RecentReviews from "../components/gymOwner/RecentReviews.vue";

export default {
  components: {
    SideBar,
    TopHeader,
    DashboardGrid,
    StatsDashboard,
    GymSchadule,
    RecentReviews,
  },
  setup() {
    const router = useRouter();
    const activePage = ref("dashboard");
    const userName = ref("");
    const selectedGymId = ref(localStorage.getItem('selectedGymId') || null);

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
      selectedGymId.value = id;
      localStorage.setItem('selectedGymId', id);
    };
    const handleTriggerAddCourse = () => router.push('/Schedule');

    return {
      router,
      activePage,
      userName,
      selectedGymId,
      switchPage,
      handleAddGym,
      handleGymSelected,
      handleTriggerAddCourse
    };
  },
  methods: {
    handleViewAllReviews() {
      this.router.push('/ReviewsPage');
    }
  }
}
</script>

<style scoped>

.dashboard-page {
  display: flex;
  padding: 32px;
  flex-direction: column;
  align-items: flex-start;
  gap: 10px;
  align-self: stretch;
  background: #FFFFFF;
}
</style>
