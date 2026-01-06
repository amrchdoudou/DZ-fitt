<template>
  <div>
    <Header />
    <AuthBackground />
    <ForgotPasswordCard/>
  </div>
</template>

<script>
import Header  from "../components/layouts/Header.vue"
import AuthBackground from "../components/layouts/AuthBackground.vue"
import ForgotPasswordCard from "../components/layouts/forgotPasswordCard.vue";

export default {
  components: {
    Header,
    AuthBackground,
    ForgotPasswordCard
  }
}
</script>
