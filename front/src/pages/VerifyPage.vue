<template>
  <div>
    <Header />
    <AuthBackground />
    <Verify/>
  </div>
</template>

<script>
import Header  from "../components/layouts/Header.vue"
import AuthBackground from "../components/layouts/AuthBackground.vue"
import Verify from "../components/layouts/VerifyCard.vue";

export default {
  components: {
    Header,
    AuthBackground,
    Verify
  }
}
</script>
