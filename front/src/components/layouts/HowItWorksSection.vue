<script setup>
import { computed } from 'vue'
import HowItWorksCard from './HowItWorksCard.vue'
import { i18n } from '../../i18n.js'
import img4 from '../../images/4.png'
import img5 from '../../images/5.png'
import img6 from '../../images/6.png'
import img7 from '../../images/7.png'
import img8 from '../../images/8.png'
import img9 from '../../images/9.png'

const $i18n = i18n;

const iconPath = (idx) => {
  const images = [img4, img5, img6, img7, img8, img9];
  return images[idx];
}

const steps = computed(() => {
  const i18nSteps = $i18n.t('how_it_works.steps');
  if (!Array.isArray(i18nSteps)) return [];
  
  return i18nSteps.map((step, index) => ({
    title: step.title,
    description: step.desc,
    img: iconPath(index)
  }));
})
</script>

<template>
  <section
    id="how-it-works"
    class="how-it-works-section"
  >
    <div class="container">
      <h2 class="section-title">
        {{ $i18n.t('how_it_works.title') }}
      </h2>
      <p class="section-subtitle">
        {{ $i18n.t('how_it_works.subtitle') }}
      </p>

      <div class="cards-grid">
        <HowItWorksCard
          v-for="step in steps"
          :key="step.title"
          :title="step.title"
          :description="step.description"
          :img="step.img"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.how-it-works-section {
  background: linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%);
  padding: 80px 20px;
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.section-title {
  text-align: center;
  font-size: clamp(32px, 6vw, 48px);
  font-weight: 700;
  color: #0940BE;
  margin: 0 0 16px 0;
  font-family: 'Roboto Flex', sans-serif;
  letter-spacing: -0.5px;
}

.section-subtitle {
  text-align: center;
  font-size: clamp(16px, 2vw, 18px);
  color: #666;
  margin: 0 0 50px 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  line-height: 1.6;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-top: 40px;
}

@media (max-width: 768px) {
  .how-it-works-section {
    padding: 60px 16px;
  }

  .cards-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}
</style>
