<template>
  <div class="stats-container">
    <!-- Utilise computedStats au lieu de stats -->
    <div class="stat-card" v-for="(stat, index) in computedStats" :key="index">
      <span class="stat-label">{{ stat.label }}</span>
      <div class="stat-value-row">
        <span class="stat-value">{{ stat.value }}</span>
        <span
          class="stat-percentage"
          :class="{ positive: stat.change > 0, negative: stat.change < 0 }"
        >
          <svg
            v-if="stat.change > 0"
            width="12"
            height="12"
            viewBox="0 0 12 12"
            fill="none"
          >
            <path
              d="M6 2.5V9.5M6 2.5L9 5.5M6 2.5L3 5.5"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
          {{ Math.abs(stat.change) }}%
        </span>
      </div>
      <span class="stat-period">{{ stat.period }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import api from "../../api";

const props = defineProps({
  selectedGymId: {
    type: [String, Number],
    required: true
  }
});

const staticData = [
  { label: "Total Profile Views", period: "last month" },
  { label: "Average rating", period: "last month" },
  { label: "Classes Published", period: "last month" },
];

const dynamicData = ref([]);
const loading = ref(false);
const error = ref(null);

const fetchStats = async () => {
  if (!props.selectedGymId) {
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    // Fetch gym details to get statistics
    const response = await api.getSalleDetail(props.selectedGymId);
    const gymData = response.data;

    // Fetch courses count
    const coursesResponse = await api.getCourses(props.selectedGymId);
    const coursesCount = coursesResponse.data?.length || 0;

    // Fetch reviews to calculate average rating
    let avgRating = 0;
    try {
      const reviewsResponse = await api.getSalleAvis(props.selectedGymId);
      const reviews = reviewsResponse.data || [];
      if (reviews.length > 0) {
        // Use note_globale from the backend or fallback to calculation
        const totalRating = reviews.reduce((sum, review) => sum + (review.note_globale || review.note || 0), 0);
        avgRating = (totalRating / reviews.length).toFixed(1);
      }
    } catch (err) {
      console.warn('Could not fetch reviews:', err);
    }

    dynamicData.value = [
      { value: gymData.views_count || 0, change: 0 },
      { value: avgRating > 0 ? `${avgRating}/5` : "-", change: 0 },
      { value: coursesCount, change: 0 },
    ];
  } catch (err) {
    console.error('Error fetching gym stats:', err);
    error.value = 'Failed to load statistics';
    dynamicData.value = [
      { value: "-", change: 0 },
      { value: "-", change: 0 },
      { value: "-", change: 0 },
    ];
  } finally {
    loading.value = false;
  }
};

const computedStats = computed(() => {
  return staticData.map((item, index) => ({
    ...item,
    value: dynamicData.value[index]?.value ?? "-",
    change: dynamicData.value[index]?.change ?? 0,
  }));
});

// Watch for selectedGymId changes
watch(() => props.selectedGymId, () => {
  fetchStats();
}, { immediate: true });

onMounted(async () => {
  await fetchStats();
});
</script>

<style scoped>
.stats-container {
  width: 100%;
  
  display: flex;
  gap: 12px;
  padding: 0px;
  background-color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.stat-card {
  height: 161px;
  display: flex;
  flex-direction: column;
  background: var(--bg-gray-dash, #F9FBFC);
  border-radius: 12px;
  padding-left: 24px;
  padding-right: 24px;
  padding-top: 24px;
  padding-bottom: 0px;
  flex: 1 0 0;
  min-width: 200px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
  gap: 31px;
}

.stat-label {
  color: var(--light-dash, #65697A);;
  font-size: 16px;
  font-weight: 600;
  line-height: 20px;
  font-style: normal;
}

.stat-value-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.stat-value {
  color:  var(--text-headlines, #040B1A);;
  font-size: 24px;
  font-weight: 600;
  line-height: 20px;
  font-style: normal;
}

.stat-percentage {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  font-style: normal;
}

.stat-percentage.positive {
  color: #00C807;
}

.stat-percentage.negative {
  color: #ef4444;
}

.stat-period {
  color:  var(--light-dash, #65697A);
  font-size: 16px;
  font-weight: 500;
  line-height: 20px;
  font-style: normal;
}
</style>
