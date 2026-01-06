<template>
  <div>
    <Header />
    <AuthBackground />
    <Reset />
  </div>
</template>

<script>
import Header from "../../components/layouts/Header.vue";
import AuthBackground from "../../components/layouts/AuthBackground.vue";
import Reset from "../../components/layouts/Reset.vue";

export default {
  components: {
    Header,
    AuthBackground,
    Reset,
  },
};
</script>
