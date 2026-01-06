<template>

  <div class="recent-reviews">

    <div class="reviewsRecentmm">

    <div class="header">
      <h2 class="title">Recent reviews</h2>
      <a href="#" @click.prevent="goToAllReviews" class="view-all-link">View all</a>
    </div>
    


    <!-- Empty State -->
    <div  class="empty-state">
      <div class="empty-icon">
         <img 
          src="../../assets/empty-reviews.svg" 
          alt="No reviews yet" 
          class="empty-svg"
        />
      </div>
      <h2 class="empty-title">Your page is empty</h2>
      <p class="empty-description">All added reviews will be listed here</p>
    </div>


    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const recentReviews = ref([])


const goToAllReviews = () => {
  router.push('/ReviewsPage')
}


const fetchRecentReviews = async () => {
  await new Promise(resolve => setTimeout(resolve, 500))
  
  // Return empty array to show empty state, or uncomment data to show reviews
    return []

  
}

// onMounted(async () => {
//   try {
//     loading.value = true
//     recentReviews.value = await fetchRecentReviews()
//   } catch (e) {
//     console.error('Error loading reviews:', e)
//   } finally {
//     loading.value = false
//   }
// })
</script>

<style scoped>
.recent-reviews {
  width: 100%;
  display: flex;


  padding: 0px;
  background: #ffffff;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.reviewsRecentmm {
  width: 100%;
   height: 320px;
  
  display: flex;
padding: 24px 16px;
flex-direction:   column;

gap: 24px;
align-self: stretch;
border-radius: 12px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--bg-gray-dash, #F9FBFC);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

.header {

padding-bottom: 12px;
padding-top: 12px;
padding-left: 16px;
padding-right: 24px;

  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.title {
  font-size: 24px;
  font-weight: 600;
  color: var(--text-headlines, #040b1a);
  margin: 0;

  font-style: normal;
  line-height: 20px;
}

.view-all-link {
  color: var(--Color, #0039C8);
  font-size: var(--Fontsize-Body-sm, 14px);
  font-weight: 600;
  line-height: var(--Line-height-Body-sm, 20px); /* 142.857% */
  font-style: normal;
  text-decoration: none;
  transition: color 0.2s;
  cursor: pointer;
}

.view-all-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}


/* Empty State */
.empty-state {
  margin-top: -150px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
  gap: 16px;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
}

.empty-svg {
  width: 100%;
  height: 100%;
}

.empty-title {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #9ca3af;
}

</style>
