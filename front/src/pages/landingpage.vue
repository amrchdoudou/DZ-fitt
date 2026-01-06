<script setup>
import Header from '../components/layouts/Header.vue'
import HeroSection from '../components/layouts/HeroSection.vue'
import HowItWorksSection from '../components/layouts/HowItWorksSection.vue'
import AboutUsSection from '../components/layouts/AboutUsSection.vue'
</script>

<template>
  <div class="landing-page landing-page-scope">
    <Header />

    <main class="landing-main">
      <HeroSection />
      <HowItWorksSection />
      <AboutUsSection />
    </main>
  </div>
</template>

<style scoped>
.landing-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0940BE;
}

.landing-main {
  flex: 1;
}
</style>
