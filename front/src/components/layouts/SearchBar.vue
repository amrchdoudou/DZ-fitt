<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from './BaseButton.vue'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'SearchResult',
      query: { search: searchQuery.value.trim() }
    })
  } else {
    router.push({ name: 'SearchResult' })
  }
}
</script>
  
  <template>
  <form
    @submit.prevent="handleSearch"
    class="flex w-full max-w-3xl flex-col gap-3 bg-white p-2 shadow-2xl sm:flex-row sm:items-center transition-all duration-300 hover:shadow-2xl hover:shadow-primary-green/40 hover:ring-primary-green/30"
    style="border-radius: 360px;"
  >
    <input
      v-model="searchQuery"
      type="text"
      placeholder="Enter an address or area"
      class="h-10 w-full border-none bg-transparent px-5 text-sm font-medium text-primary-blue placeholder:text-primary-blue/60 focus:outline-none focus:ring-0"
      style="border-radius: 360px;"
    />

    <div class="flex justify-end sm:justify-center">
      <BaseButton type="submit" variant="filled" size="sm" class="shadow-lg">
        Search
      </BaseButton>
    </div>
  </form>
  </template>