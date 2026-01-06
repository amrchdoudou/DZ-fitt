<template>
  <nav class="navbar"> 
    <div class="left-side">
      <div class="logo">
        <router-link to="/">
          <div class="logo-text">Dz-Fit</div>
        </router-link>
      </div>
    </div>

    <!-- Centered Services -->
    <div class="services">
      <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
        <span v-if="$route.path === '/'" class="active-dot">●</span>
        {{ $i18n.t('navbar.home') }}
      </router-link>
      <router-link to="/SearchResult" class="nav-link" :class="{ active: $route.path === '/SearchResult' }">
        <span v-if="$route.path === '/SearchResult'" class="active-dot">●</span>
        {{ $i18n.t('navbar.search') }}
      </router-link>
      <a href="/#how-it-works" class="nav-link">{{ $i18n.t('navbar.how_it_works') }}</a>
      <a href="/#about-us" class="nav-link">{{ $i18n.t('navbar.about_us') }}</a>
    </div>

    <div class="right-side">
      <!-- Language Switcher -->
      <div class="lang-selector" @click.stop="toggleLangDropdown" v-click-outside="closeLangDropdown">
        <div class="lang-trigger">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" class="globe-icon">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
          </svg>
          <span class="lang-arrow">⌵</span>
        </div>
        <div v-if="langDropdownOpen" class="dropdown-menu lang-menu">
          <div class="dropdown-item" :class="{ active: $i18n.locale === 'en' }" @click="setLang('en')">English</div>
          <div class="dropdown-item" :class="{ active: $i18n.locale === 'fr' }" @click="setLang('fr')">Français</div>
          <div class="dropdown-item" :class="{ active: $i18n.locale === 'ar' }" @click="setLang('ar')">العربية</div>
        </div>
      </div>

      <!-- Auth Section -->
      <div v-if="!user" class="auth-buttons">
        <router-link to="/login">
          <button class="login-btn">{{ $i18n.t('navbar.login') }}</button>
        </router-link>
        <router-link to="/signup">
          <button class="signup-btn">{{ $i18n.t('navbar.signup') }}</button>
        </router-link>
      </div>

      <div v-else class="user-profile" @click.stop="toggleUserDropdown" v-click-outside="closeUserDropdown">
        <span class="user-name">{{ userFullName }}</span>
        <span class="dropdown-arrow">⌵</span>
        
        <div v-if="userDropdownOpen" class="dropdown-menu user-menu">
          <div class="dropdown-item logout-item" @click="handleLogout">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" class="logout-icon">
              <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
            </svg>
            {{ $i18n.t('navbar.logout') }}
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { i18n } from '../../i18n.js';

export default {
  name: 'HeaderComponent',
  data() {
    return {
      user: null,
      userDropdownOpen: false,
      langDropdownOpen: false,
    }
  },
  computed: {
    $i18n() {
      return i18n;
    },
    userFullName() {
      try {
        const profilStr = localStorage.getItem('profil');
        let name = '';
        
        // 1. Try profile data first
        if (profilStr) {
          const profil = JSON.parse(profilStr);
          name = profil.nom_complet || 
                 profil.full_name || 
                 (profil.prenom && profil.nom ? `${profil.prenom} ${profil.nom}` : '') ||
                 profil.nom ||
                 profil.prenom;
        }

        // 2. Fallback to user object
        if (!name && this.user) {
          name = this.user.nom_complet || 
                 this.user.full_name || 
                 (this.user.first_name || this.user.last_name ? `${this.user.first_name || ''} ${this.user.last_name || ''}`.trim() : '') ||
                 this.user.username;
        }

        // 3. Extract name from email if needed
        if (!name && this.user && this.user.email) {
          const emailPrefix = this.user.email.split('@')[0];
          // Determine if prefix looks like a name (e.g. r_keghouche -> R Keghouche)
          name = emailPrefix.replace(/[._-]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        }

        // 4. Last fallback
        return name && name.trim() ? name : (this.user ? this.user.email : 'User');
      } catch (e) {
        // Emergency fallback: extract from email if available
        if (this.user && this.user.email) {
           return this.user.email.split('@')[0].replace(/[._-]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        }
        return 'User';
      }
    }
  },
  methods: {
    checkUser() {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        try {
          this.user = JSON.parse(userStr);
        } catch (e) {
          this.user = null;
        }
      } else {
        this.user = null;
      }
    },
    toggleUserDropdown() {
      this.userDropdownOpen = !this.userDropdownOpen;
      if (this.userDropdownOpen) this.langDropdownOpen = false;
    },
    closeUserDropdown() {
      this.userDropdownOpen = false;
    },
    toggleLangDropdown() {
      this.langDropdownOpen = !this.langDropdownOpen;
      if (this.langDropdownOpen) this.userDropdownOpen = false;
    },
    closeLangDropdown() {
      this.langDropdownOpen = false;
    },
    setLang(lang) {
      this.$i18n.setLocale(lang);
      this.langDropdownOpen = false;
    },
    handleLogout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('user');
      localStorage.removeItem('profil');
      localStorage.removeItem('selectedGymId');
      this.user = null;
      this.$router.push('/login');
    }
  },
  mounted() {
    this.checkUser();
    window.addEventListener('storage', this.checkUser);
  },
  unmounted() {
    window.removeEventListener('storage', this.checkUser);
  },
  directives: {
    'click-outside': {
      mounted(el, binding) {
        el.clickOutsideEvent = function (event) {
          if (!(el === event.target || el.contains(event.target))) {
            binding.value(event);
          }
        };
        document.body.addEventListener('click', el.clickOutsideEvent);
      },
      unmounted(el) {
        document.body.removeEventListener('click', el.clickOutsideEvent);
      },
    }
  },
  watch: {
    '$route'() {
      this.checkUser();
      this.userDropdownOpen = false;
      this.langDropdownOpen = false;
    }
  }
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  height: 80px;
  background-color: #0940BE;
  color: white;
  position: relative;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  font-family: 'Inter', sans-serif;
  flex-shrink: 0;
}

.left-side {
  flex: 0 0 auto;
}

.logo-text {
  font-size: 26px;
  font-weight: 800;
  color: white;
  text-decoration: none;
}

.logo a {
  text-decoration: none;
}

.services {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 48px;
  white-space: nowrap;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 400;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  position: relative;
  opacity: 0.85;
}

.nav-link:hover {
  opacity: 1;
}

.nav-link.active {
  color: #B3F90F;
  font-weight: 700;
  opacity: 1;
}

.active-dot {
  font-size: 18px;
  color: #B3F90F;
  line-height: 1;
  display: inline-block;
  margin-right: -2px;
}

.right-side {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 24px;
}

.auth-buttons {
  display: flex;
  gap: 12px;
}

.login-btn, .signup-btn {
  height: 44px;
  padding: 0 24px;
  border-radius: 22px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.login-btn {
  background-color: transparent;
  color: #B3F90F;
  border: 1.5px solid #B3F90F;
}

.login-btn:hover {
  background: rgba(179, 249, 15, 0.1);
}

.signup-btn {
  background-color: #B3F90F;
  color: #000;
  border: none;
}

.signup-btn:hover {
  background-color: #a0e00d;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 24px;
  transition: background 0.2s;
  position: relative;
  background: rgba(255, 255, 255, 0.05);
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.12);
}

.user-name {
  font-weight: 600;
  font-size: 15px;
}

.dropdown-arrow {
  font-size: 12px;
  opacity: 0.8;
}

.lang-selector {
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 20px;
  transition: background 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
}

.lang-selector:hover {
  background: rgba(255, 255, 255, 0.12);
}

.lang-trigger {
  display: flex;
  align-items: center;
  gap: 4px;
}

.lang-arrow {
  font-size: 18px;
  font-weight: 600;
  color: white;
  line-height: 1;
  margin-bottom: 2px;
}

.globe-icon {
  opacity: 1;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 12px);
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.18);
  min-width: 180px;
  padding: 8px;
  overflow: hidden;
  z-index: 1100;
  animation: slideDown 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.dropdown-item {
  padding: 12px 16px;
  color: #333;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 12px;
}

.dropdown-item:hover {
  background: #f0f2f5;
  color: #0940BE;
}

.dropdown-item.active {
  background: #eef3ff;
  color: #0940BE;
  font-weight: 700;
}

.logout-item {
  color: #F9191C;
  border-top: 1px solid #eee;
  border-radius: 0 0 8px 8px;
  margin-top: 4px;
}

.logout-item:hover {
  background: #FFF5F5;
  color: #F9191C;
}

.lang-menu {
  min-width: 140px;
}

:root[dir="rtl"] .services {
  flex-direction: row-reverse;
}

:root[dir="rtl"] .active-dot {
  margin-right: 0;
  margin-left: -2px;
}

:root[dir="rtl"] .dropdown-menu {
  right: auto;
  left: 0;
}

@media (max-width: 1024px) {
  .services {
    gap: 32px;
  }
}

@media (max-width: 850px) {
  .services {
    display: none;
  }
}
</style>
