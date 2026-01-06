<script setup>
const props = defineProps({
  title: String,
  description: String,
  img: String, // e.g. "/4.png"
})
</script>

<template>
  <article
    class="group relative flex min-h-[480px] flex-col overflow-hidden rounded-2xl bg-white shadow-lg ring-1 ring-primary-blue/10 transition-all duration-300 hover:shadow-xl hover:shadow-primary-green/10 hover:-translate-y-1"
  >
    <!-- Image area - properly sized to show full image -->
    <div
      class="relative flex h-[240px] items-center justify-center overflow-hidden bg-light-bg"
    >
      <img
        v-if="img"
        :src="img"
        :alt="title"
        class="h-full w-full object-contain transition-transform duration-300 group-hover:scale-105"
      />
    </div>

    <!-- Content area -->
    <div class="flex flex-1 flex-col justify-between gap-4 p-6">
      <div class="space-y-3">
        <h3 class="card-title">
          {{ title }}
        </h3>
        <p class="card-description">
          {{ description }}
        </p>
      </div>
    </div>
  </article>
</template>

<style scoped>
.card-title {
  font-size: clamp(18px, 2.5vw, 22px);
  font-weight: 700;
  color: #0940BE;
  transition: color 0.3s;
  line-height: 1.3;
}

.group:hover .card-title {
  color: #B3F90F;
}

.card-description {
  font-size: clamp(14px, 1.8vw, 16px);
  line-height: 1.7;
  color: rgba(9, 64, 190, 0.8);
}
</style>
