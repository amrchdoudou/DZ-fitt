<template>
  <div class="reset-container">
    <!-- Bouton Retour -->
    <button class="back-btn" @click="$router.back()">←</button>

    <h1>Reset password</h1>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>

    <!-- Champ Nouveau mot de passe -->
    <div class="input-group">
      <label>New Password</label>
      <input 
        type="password" 
        v-model="newPassword" 
        placeholder="Enter new password (min. 8 characters)"
        :disabled="loading"
      />
    </div>

    <!-- Champ Confirmer -->
    <div class="input-group">
      <label>Confirm New Password</label>
      <input 
        type="password" 
        v-model="confirmPassword" 
        placeholder="Confirm new password"
        :disabled="loading"
      />
    </div>

    <!-- LE BOUTON -->
    <button 
      class="submit-btn" 
      @click="submitReset"
      :disabled="loading"
    >
      {{ loading ? 'Resetting...' : 'Submit' }}
    </button>

    <p class="legal-text">
      By clicking 'Submit', you acknowledge that you have read and accept the Terms of Service and Privacy Policy.
    </p>
  </div>
</template>

<script>
import api from '../../api.js';

export default {
  name: 'ResetPassword',
  data() {
    return {
      newPassword: '',
      confirmPassword: '',
      email: this.$route.query.email || '',
      resetToken: this.$route.query.token || '',  // ✅ FIX : récupérer "token" pas "reset_token"
      loading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async submitReset() {
      // Vérification basique
      if (this.newPassword === '' || this.confirmPassword === '') {
        this.errorMessage = "Please fill in all fields";
        return;
      }

      if (this.newPassword.length < 8) {
        this.errorMessage = "Password must be at least 8 characters";
        return;
      }

      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = "Passwords do not match!";
        return;
      }

      if (!this.email || !this.resetToken) {
        this.errorMessage = "Invalid reset link - Missing email or token";
        console.error('❌ Missing data:', {
          email: this.email,
          token: this.resetToken
        });
        return;
      }

      this.loading = true;
      this.errorMessage = '';

      console.log('📤 Sending reset request:', {
        email: this.email,
        token: this.resetToken,
        password_length: this.newPassword.length
      });

      try {
        const response = await api.resetPassword({
          reset_token: this.resetToken,  // ✅ Envoyer "reset_token" au backend
          new_password: this.newPassword,
          confirm_password: this.confirmPassword
        });

        const data = response.data;

        // ✅ Log pour debug
        console.log('📥 Response status:', response.status);
        console.log('📥 Response data:', data);

        this.successMessage = "✅ Password reset successfully!";
          
        setTimeout(() => {
          this.$router.push({
            path: '/login',
            query: { email: this.email }
          });
        }, 2000);

      } catch (error) {
        console.error("❌ Reset error:", error);
        
        if (error.response?.data) {
          const data = error.response.data;
          
          if (data.reset_token) {
            this.errorMessage = Array.isArray(data.reset_token) 
              ? data.reset_token[0] 
              : data.reset_token;
          } else if (data.new_password) {
            this.errorMessage = Array.isArray(data.new_password) 
              ? data.new_password[0] 
              : data.new_password;
          } else if (data.error) {
            this.errorMessage = data.error;
          } else {
            this.errorMessage = "Failed to reset password";
          }
          console.error('❌ Server error:', data);
        } else {
          this.errorMessage = "Connection error. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    // ✅ Debug : Afficher les paramètres reçus
    console.log('🔍 Reset page mounted with:', {
      email: this.email,
      token: this.resetToken,
      hasEmail: !!this.email,
      hasToken: !!this.resetToken
    });

    if (!this.email || !this.resetToken) {
      console.error('❌ Missing email or token, redirecting...');
      this.$router.push('/forgot-password');
    }
  }
}
</script>
<style scoped>
.reset-container {
  max-width: 500px;
  margin: 60px auto;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
}

.back-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

h1 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 10px;
}

.error-message {
  background: #fee;
  color: #c00;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  border: 1px solid #fcc;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 12px;
  border-radius: 8px;
  font-size: 14px;
  border: 1px solid #c3e6cb;
}

.input-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.input-group label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
}

input {
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  background: #f5f5f7;
  font-size: 14px;
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.submit-btn {
  background: #c8ff32;
  color: black;
  padding: 12px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: 0.2s;
}

.submit-btn:hover:not(:disabled) {
  opacity: 0.8;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.legal-text {
  font-size: 12px;
  color: #777;
  text-align: center;
  line-height: 1.5;
}
</style>