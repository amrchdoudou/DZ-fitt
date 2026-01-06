<template>
  <div>
    <Header />
    <AuthBackground />
    <SignupCard />
  </div>
</template>

<script>
import Header  from "../components/layouts/Header.vue"
import AuthBackground from "../components/layouts/AuthBackground.vue"
import SignupCard from "../components/layouts/SignupCard.vue";

export default {
  components: {
    Header,
    AuthBackground,
    SignupCard
  }
}
</script>
