<template>
  <div class="top_header">
    <div class="grey-header">
      <div class="rectangle">
        <p class="profile-name">{{ userFullName }}</p>
      </div>
    </div>    
  </div>    
</template>

<script setup>
import { computed } from 'vue';
import { i18n } from '../../i18n.js';

const userFullName = computed(() => {
  try {
    const userStr = localStorage.getItem('user');
    const profilStr = localStorage.getItem('profil');
    
    let name = '';
    
    // 1. Try profile data first (often has specific names)
    if (profilStr) {
      const profil = JSON.parse(profilStr);
      name = profil.nom_complet || 
             profil.full_name || 
             (profil.prenom && profil.nom ? `${profil.prenom} ${profil.nom}` : '') ||
             profil.nom ||
             profil.prenom;
    }
    
    // 2. Fallback to user object
    if (!name && userStr) {
      const user = JSON.parse(userStr);
      name = user.nom_complet || 
             user.full_name || 
             (user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : '') ||
             user.username;
    }

    // 3. Extract name from email if needed
    if (!name && userStr) {
      const u = JSON.parse(userStr);
      if (u.email) {
          const emailPrefix = u.email.split('@')[0];
          name = emailPrefix.replace(/[._-]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      }
    }

    // 4. Last fallback
    return name && name.trim() ? name : (userStr ? JSON.parse(userStr).email : 'Gym Owner');
  } catch (e) {
    return 'Gym Owner';
  }
});
</script>

<style scoped>
/* ===== TOP WHITE HEADER ===== */
.grey-header {
  width: 96%;
  height: 50px;
  background-color: #f7f7f7;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-right: 40px;
  box-shadow: 0px 1px 3px rgba(0,0,0,0.05);
}

.rectangle {
  background: #ffffff;
  padding: 0px 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
}

.profile-name {
  font-size: 11px;
  color: #4a4a4a;
  text-transform: capitalize;
  font-weight: 500;
}

:root[dir="rtl"] .grey-header {
  justify-content: flex-start;
  padding-right: 0;
  padding-left: 40px;
}
</style>
