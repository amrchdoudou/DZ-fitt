import { createRouter, createWebHistory } from 'vue-router';
import Login from '../pages/auth/LoginPage.vue';
import SignUp from '../pages/auth/SignUpPage.vue';
import ForgotPassword from '../pages/auth/ForgotPasswordPage.vue';
import Reset from '../pages/auth/ResetPage.vue';
import Verify from '../pages/auth/VerifyPage.vue';
import MyGym from '../pages/gymOwnerPages/MyGym.vue';
import LandingPage from '../pages/landingpage.vue';

import SearchResult from "../pages/SearchResult.vue";

import DashboardEmpty from "../pages/DashboardEmpty.vue";
import ReviewsPage from "../pages/ReviewsPage.vue";
import SchedulePage from "../pages/SchedulePage.vue";
import GymProfile from "../pages/GymProfile.vue";

import DashboardPagem from "../pages/DashboardPagem.vue";

import ProfilePage from '../pages/ProfilPage.vue';

// ✅ ADD THIS: Import AuthCallback component
import AuthCallback from '../components/AuthCallback.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
    alias: '/LandingPage'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login  // ✅ FIXED: Was "LoginComponent", should be "Login"
  },
  {
    path: '/auth/callback',
    name: 'AuthCallback',
    component: AuthCallback  // ✅ NOW THIS WILL WORK
  },
  { path: '/signup', name: 'SignUp', component: SignUp },
  { path: '/forgot-password', name: 'ForgotPassword', component: ForgotPassword },
  { path: '/reset-password', name: 'ResetPassword', component: Reset },
  { path: '/verify', name: 'VerifyPage', component: Verify },
  {
    path: '/gym/:id',
    name: 'GymProfile',
    component: ProfilePage
  },
  {
    path: '/MyGym',
    name: 'MyGym',
    component: MyGym,
    meta: { requiresAuth: true, requiresGerant: true }
  },
  {
    name: "SearchResult",
    path: "/SearchResult",
    component: SearchResult,
    meta: {
      title: "SearchResult",
    },
  },

  {
    name: "DashboardPagem",
    path: "/Dashboardm",
    component: DashboardPagem,
    meta: {
      title: "DashboardPagem",
      requiresAuth: true,
      requiresGerant: true
    },
  },

  {
    name: "DashboardEmpty",
    path: "/DashboardEmpty",
    component: DashboardEmpty,
    meta: {
      title: "DashboardEmpty",
      requiresAuth: true,
      requiresGerant: true
    },
  },
  {
    name: "ReviewsPage",
    path: "/ReviewsPage",
    component: ReviewsPage,
    meta: {
      title: "ReviewsPage",
      requiresAuth: true,
      requiresGerant: true
    },
  },
  {
    name: "SchedulePage",
    path: "/Schedule",
    component: SchedulePage,
    meta: {
      title: "SchedulePage",
      requiresAuth: true,
      requiresGerant: true
    },
  },

  {
    name: "ProfilePage",
    path: "/ProfilePage",
    component: ProfilePage,
    meta: {
      title: "ProfilePage",
    },
  },

];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      }
    } else if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
});

// Garde de navigation pour protéger les routes authentifiées
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('authToken');
  const userStr = localStorage.getItem('user');

  // ✅ ALLOW /auth/callback without authentication check
  if (to.path === '/auth/callback') {
    next();
    return;
  }

  // Si la route nécessite une authentification
  if (to.meta.requiresAuth) {
    if (!token || !userStr) {
      // Pas authentifié, rediriger vers login
      console.log('🚫 Not authenticated, redirecting to login');
      next('/login');
      return;
    }

    try {
      const user = JSON.parse(userStr);

      // Si la route nécessite un profil gérant
      if (to.meta.requiresGerant && user.type_utilisateur !== 'gerant') {
        console.log('🚫 Not a gerant, redirecting to login');
        next('/login');
        return;
      }
    } catch (e) {
      console.error('Error parsing user data:', e);
      next('/login');
      return;
    }
  }

  // Si déjà authentifié et on essaie d'accéder à /login, rediriger vers MyGym
  if (to.path === '/login' && token && userStr) {
    try {
      const user = JSON.parse(userStr);
      if (user.type_utilisateur === 'gerant') {
        console.log('✅ Already authenticated as gerant, redirecting to MyGym');
        next('/MyGym');
        return;
      }
    } catch (e) {
      // Si erreur, continuer normalement
    }
  }

  next();
});

export default router;