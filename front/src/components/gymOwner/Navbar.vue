<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-logo">
        <router-link to="/">DZ-Fit</router-link>
      </div>
      
      <div class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/SearchResult" class="nav-link">Search</router-link>
        <router-link to="/Dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/Schedule" class="nav-link">Schedule</router-link>
        <router-link to="/login" class="nav-link nav-link-login">Login</router-link>
        <router-link to="/signup" class="nav-link nav-link-signup">Sign Up</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo a {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2563eb;
  text-decoration: none;
  transition: color 0.3s ease;
}

.navbar-logo a:hover {
  color: #1d4ed8;
}

.navbar-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  padding: 0.5rem 1rem;
  border-radius: 8px;
}

.nav-link:hover {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.1);
}

.nav-link-login {
  color: #2563eb;
  border: 1px solid #2563eb;
}

.nav-link-login:hover {
  background: #2563eb;
  color: white;
}

.nav-link-signup {
  background: #2563eb;
  color: white;
}

.nav-link-signup:hover {
  background: #1d4ed8;
}
</style>
