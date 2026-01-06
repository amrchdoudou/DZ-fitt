<template>
  <div>
    <Header />
    <AuthBackground />
    <LoginCard />
  </div>
</template>

<script>
import Header  from "../components/layouts/Header.vue"
import AuthBackground from "../components/layouts/AuthBackground.vue"
import LoginCard from "../components/layouts/LoginCard.vue";

export default {
  components: {
    Header,
    AuthBackground,
    LoginCard
  }
}
</script>
