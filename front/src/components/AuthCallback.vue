<template>
  <div class="callback-container">
    <div class="callback-card">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <h2>Completing sign in...</h2>
        <p>Please wait while we log you in</p>
      </div>
      <div v-else-if="error" class="error-state">
        <h2>Login Failed</h2>
        <p>{{ error }}</p>
        <button @click="goToLogin" class="retry-btn">Return to Login</button>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api.js'; // Adjust path if your api.js is elsewhere

export default {
  name: 'AuthCallback',
  data() {
    return {
      loading: true,
      error: ''
    }
  },
  async mounted() {
    await this.handleCallback();
  },
  methods: {
    async handleCallback() {
      try {
        // Get token from URL if provided (from our updated adapters.py)
        const urlParams = new URLSearchParams(window.location.search);
        const tokenFromUrl = urlParams.get('token');
        
        const fetchHeaders = {
          'Content-Type': 'application/json',
        };

        if (tokenFromUrl) {
          fetchHeaders['Authorization'] = `Token ${tokenFromUrl}`;
        }

        // Get user info from the session or token
        const response = await fetch('http://localhost:8000/api/user/', {
          method: 'GET',
          credentials: 'include', // includes cookies for session auth
          headers: fetchHeaders
        });

        console.log('📥 Response status:', response.status);

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          console.error('❌ Response not OK:', errorData);
          throw new Error(errorData.error || 'Failed to get user information');
        }

        const data = await response.json();
        console.log('✅ User data received:', data);
        
        if (!data.token || !data.user) {
          console.error('❌ Invalid data structure:', data);
          throw new Error('Invalid authentication response');
        }

        // Store authentication data
        localStorage.setItem('authToken', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        if (data.profil) {
          localStorage.setItem('profil', JSON.stringify(data.profil));
        }

        console.log('💾 Data stored in localStorage');

        // Set token for future API calls
        if (typeof api.setAuthToken === 'function') {
          api.setAuthToken(data.token);
          console.log('🔑 Auth token set in API');
        }

        // Redirect based on user type
        console.log('🔄 Redirecting user...');
        setTimeout(() => {
          if (data.user.type_utilisateur === 'gerant') {
            console.log('➡️ Redirecting to /MyGym');
            this.$router.replace('/MyGym');
          } else if (data.user.type_utilisateur === 'client') {
            console.log('➡️ Redirecting to home');
            this.$router.replace('/');
          } else {
            console.log('➡️ Redirecting to home (default)');
            this.$router.replace('/');
          }
        }, 500);

      } catch (err) {
        console.error('❌ OAuth callback error:', err);
        this.loading = false;
        this.error = err.message || 'Authentication failed. Please try again.';
      }
    },

    goToLogin() {
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.callback-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f5f7;
}

.callback-card {
  background: white;
  border-radius: 20px;
  padding: 60px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  text-align: center;
  max-width: 500px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #0044ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.loading p {
  font-size: 16px;
  color: #777;
  margin: 0;
}

.error-state h2 {
  font-size: 24px;
  font-weight: 600;
  color: #c00;
  margin-bottom: 15px;
}

.error-state p {
  font-size: 16px;
  color: #666;
  margin-bottom: 25px;
}

.retry-btn {
  padding: 12px 30px;
  background: #0044ff;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.retry-btn:hover {
  opacity: 0.9;
}
</style>