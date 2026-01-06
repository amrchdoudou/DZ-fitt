<template>
  <div class="signup-card">
    <div class="first-part">
      <h1>Log in</h1>

      <!-- Success/Error Messages -->
      <div v-if="successMessage" class="message success-message">
        {{ successMessage }}
      </div>
      <div v-if="error" class="message error-message">
        {{ error }}
      </div>

      <!-- GOOGLE LOGIN BUTTON -->
      <div class="signupWithGoogle">
        <button class="google-btn" @click="handleGoogleLogin" :disabled="loading">
          <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" class="google-icon" />
          Log in with Google
        </button>
      </div>
    </div>

    <div class="middile">
      <p>Or log in with email</p>
    </div>

    <div class="last-part">
      <form class="signup-form" @submit.prevent="handleLogin">
        <p>Email address</p>
        <input 
          type="email" 
          placeholder="Email" 
          class="input-field"
          v-model="email"
          :disabled="loading"
          required
        />
        <p>Password</p>
        <input 
          type="password" 
          placeholder="Password" 
          class="input-field"
          v-model="password"
          :disabled="loading"
          required
        />
        <button 
          type="submit" 
          class="continue-btn"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Continue' }}
        </button>
      </form>
      <p>Don't have an account? 
        <router-link to="/signup">Sign up</router-link>
      </p>
      <p class="forgot-password">
        <a href="/forgot-password">Forgot password?</a>
      </p>
      <p class="terms">
        By clicking 'Continue', you acknowledge that you have read and accept the 
        <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
      </p>
    </div>
  </div>
</template>

<script>
import api from '../../api.js';

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: '',
      successMessage: ''
    }
  },
  methods: {
     handleGoogleLogin() {
  window.location.href = 'http://localhost:8000/api/google-auth/';
},


    async handleLogin(event) {
      if (event) event.preventDefault();

      if (!this.email || !this.password) {
        this.error = 'Please fill in all fields';
        return;
      }

      if (this.password.length < 8) {
        this.error = 'Password must be at least 8 characters';
        return;
      }

      this.loading = true;
      this.error = '';

      try {
        const response = await api.login({
          email: this.email,
          password: this.password
        });

        const { token, user, profil } = response.data;

        if (!token || !user) {
          this.error = 'Invalid server response';
          return;
        }

        // Store authentication data
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(user));
        if (profil) {
          localStorage.setItem('profil', JSON.stringify(profil));
        }

        api.setAuthToken(token);

        // Redirect based on user type
        if (user.type_utilisateur === 'gerant') {
          this.$router.replace('/MyGym');
        } else if (user.type_utilisateur === 'client') {
          this.$router.replace('/');
        } else {
          this.$router.replace('/');
        }

      } catch (err) {
        console.error('Login error:', err);
        
        if (err.response) {
          const data = err.response.data;
          let errorMessage = '';
          
          if (data.non_field_errors) {
            errorMessage = Array.isArray(data.non_field_errors) 
              ? data.non_field_errors[0] 
              : data.non_field_errors;
          } else if (data.error) {
            errorMessage = typeof data.error === 'string' 
              ? data.error 
              : (Array.isArray(data.error) ? data.error[0] : JSON.stringify(data.error));
          } else if (data.detail) {
            errorMessage = data.detail;
          } else if (data.message) {
            errorMessage = data.message;
          } else {
            errorMessage = 'Login failed. Please check your credentials.';
          }
          
          this.error = errorMessage;
        } else if (err.request) {
          this.error = 'Connection error. Please check your internet connection.';
        } else {
          this.error = 'Error: ' + err.message;
        }
      } finally {
        this.loading = false;
      }
    }
  },

  mounted() {
    // Check for Google OAuth error in URL params
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('error')) {
      this.error = 'Google login failed. Please try again.';
    }
  }
}
</script>

<style scoped>
/* Messages */
.message {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.success-message {
  background: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.error-message {
  background: #fee;
  color: #c00;
  border: 1px solid #fcc;
}

/* Rest of your existing styles... */
.signup-card {
  width: 650px;
  background: #ffffff;
  border-radius: 25px;
  padding: 40px 50px;
  margin: 60px auto;
  box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.12);
  text-align: center;
  font-family: "Inter", sans-serif;
}

.signup-card h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 25px;
  color: #000000;
}

.google-btn {
  width: 100%;
  padding: 12px;
  border-radius: 30px;
  background: white;
  border: 1px solid #ddd;
  font-size: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.google-btn:hover:not(:disabled) {
  background: #f7f7f7;
}

.google-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-icon {
  width: 20px;
  height: 20px;
}

.middile {
  margin: 30px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.middile p {
  background: white;
  padding: 0 15px;
  font-size: 14px;
  color: #777;
}

.middile::before,
.middile::after {
  content: "";
  height: 1px;
  background: #ddd;
  width: 35%;
  position: absolute;
  top: 50%;
}

.middile::before { left: 0; }
.middile::after { right: 0; }

.signup-form {
  text-align: left;
}

.signup-form p {
  font-size: 14px;
  font-weight: 600;
  margin: 15px 0 5px;
}

.input-field {
  width: 95%;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  background: #f5f5f7;
  margin-bottom: 10px;
  font-size: 14px;
}

.input-field:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.continue-btn {
  width: 180px;
  padding: 12px;
  background: #c8ff32;
  border-radius: 25px;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  display: block;
  margin: 15px auto 0 auto;
}

.continue-btn:hover:not(:disabled) {
  opacity: 0.8;
}

.continue-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.forgot-password {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}

.forgot-password a {
  color: #0044ff;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;
}

.forgot-password a:hover {
  opacity: 0.8;
}

.terms {
  margin-top: 20px;
  font-size: 12px;
  color: #777;
  text-align: center;
  line-height: 1.5;
}

.terms a {
  color: #0044ff;
}
</style>