<template>
  <div class="background-container">
    <img :src="imageUrl" class="background-image" />
  </div>
</template>

<script>
import bgImage from '../../images/Background.png'  // ✅ Use import instead of require

export default {
  name: 'AuthBackground',
  data() {
    return {
      imageUrl: bgImage
    }
  }
}
</script>

<style scoped>
.background-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: -1;
}


.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
