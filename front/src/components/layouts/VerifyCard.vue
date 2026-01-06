<template>
  <div class="verify-card">
    <!-- Back Arrow -->
    <div class="back-arrow" @click="$router.back()">←</div>

    <h1>Verify your email address</h1>

    <p class="desc">
      We sent you a 4 digit code to verify<br>
      your email address <span class="email">{{ email }}</span>.<br>
      Enter it in the field below.
    </p>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- 4 input boxes -->
    <div class="code-container">
      <input
        v-for="(digit, index) in 4"
        :key="index"
        maxlength="1"
        type="text"
        inputmode="numeric"
        class="code-box"
        v-model="code[index]"
        :ref="el => { if (el) inputs[index] = el }"
        @input="handleInput(index, $event)"
        @keydown="handleKeydown(index, $event)"
        :disabled="loading"
      />
    </div>

    <!-- Resend -->
    <p class="resend">
      Didn't get the code? 
      <a href="#" @click.prevent="resendCode" :class="{ disabled: loading }">
        {{ loading ? 'Sending...' : 'Resend' }}
      </a>
    </p>

    <!-- Submit button -->
    <button 
      class="submit-btn" 
      @click="submitCode"
      :disabled="loading || code.join('').length !== 4"
    >
      {{ loading ? 'Verifying...' : 'Submit' }}
    </button>

    <!-- Terms -->
    <p class="terms">
      By clicking 'Submit', you acknowledge that you have read and accept the 
      <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
    </p>
  </div>
</template>

<script>
import api from '../../api';

export default {
  name: "VerifyEmailCard",
  data() {
    return {
      email: this.$route.query.email || "",
      code: ["", "", "", ""],
      inputs: [],
      loading: false,
      error: "",
      isFromForgotPassword: this.$route.query.from === 'forgot-password'
    };
  },
  methods: {
    handleInput(index, event) {
      const value = event.target.value;
      
      if (!/^\d*$/.test(value)) {
        this.code[index] = "";
        return;
      }

      this.code[index] = value;
      this.error = "";

      if (value && index < 3) {
        this.inputs[index + 1]?.focus();
      }
    },

    handleKeydown(index, event) {
      if (event.key === 'Backspace' && !this.code[index] && index > 0) {
        this.inputs[index - 1]?.focus();
      }
    },

    async submitCode() {
  const enteredCode = this.code.join("");
  
  if (enteredCode.length !== 4) {
    this.error = "Please enter the 4-digit code";
    return;
  }

  if (!this.email) {
    this.error = "Email is missing";
    return;
  }

  this.loading = true;
  this.error = "";

  try {
    // ✅ Si venant de Forgot Password
    if (this.isFromForgotPassword) {
      const response = await api.verifyResetCode({
        email: this.email,
        code: enteredCode
      });

      const data = response.data;
      
      // ✅ DEBUG : Voir ce que le backend retourne
      console.log('🔍 Backend response:', data);

      // ✅ FIX : Vérifier que reset_token existe bien
      if (!data.reset_token) {
        console.error('❌ No reset_token in response:', data);
        this.error = "Server error: Missing reset token";
        return;
      }

      console.log('✅ Reset token received:', data.reset_token);

      // ✅ Rediriger avec le token
      this.$router.push({
        path: '/reset-password',
        query: { 
          email: this.email,
          token: data.reset_token  // ✅ Utiliser exactement "reset_token"
        }
      });
    } 
    // Si venant de Signup (code existant)
    else {
      const response = await api.verifyEmail({
        email: this.email,
        code: enteredCode
      });

      console.log("✅ Verification success:", response.data);

      const { user, can_login, needs_approval } = response.data;

      if (user.type_utilisateur === 'gerant' && needs_approval) {
        this.$router.push('/pending-approval');
      } else if (can_login) {
        this.$router.push({
          path: '/login',
          query: { 
            email: this.email,
            verified: 'true'
          }
        });
      }
    }

  } catch (err) {
    console.error("❌ Verification error:", err);
    
    if (err.response?.data) {
      const errorData = err.response.data;
      
      if (typeof errorData === 'string') {
        this.error = errorData;
      } else if (errorData.non_field_errors) {
        this.error = errorData.non_field_errors[0];
      } else if (errorData.detail) {
        this.error = errorData.detail;
      } else if (errorData.error) {
        this.error = errorData.error;
      } else {
        this.error = "Invalid verification code";
      }
    } else {
      this.error = "Connection error. Please try again.";
    }

    this.code = ["", "", "", ""];
    this.$nextTick(() => {
      this.inputs[0]?.focus();
    });
  } finally {
    this.loading = false;
  }
},

    async resendCode() {
      if (this.loading) return;

      if (!this.email) {
        this.error = "Email is missing";
        return;
      }

      this.loading = true;
      this.error = "";

      try {
        if (this.isFromForgotPassword) {
          // Renvoyer vers forgot-password pour renvoyer le code
          await api.forgotPassword({ email: this.email });

          alert(`A new code has been sent to ${this.email}`);
          this.code = ["", "", "", ""];
          this.$nextTick(() => {
            this.inputs[0]?.focus();
          });
        } else {
          const response = await api.resendVerificationCode({
            email: this.email
          });

          console.log("✅ Resend success:", response.data);
          alert(`A new code has been sent to ${this.email}`);

          this.code = ["", "", "", ""];
          this.$nextTick(() => {
            this.inputs[0]?.focus();
          });
        }

      } catch (err) {
        console.error("❌ Resend error:", err);
        
        if (err.response?.data?.error) {
          this.error = err.response.data.error;
        } else {
          this.error = "Failed to resend code. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    }
  },
  mounted() {
    if (!this.email) {
      this.$router.push('/login');
      return;
    }

    this.$nextTick(() => {
      this.inputs[0]?.focus();
    });
  }
};
</script>

<style scoped>
.verify-card {
  width: 650px;
  background: #fff;
  border-radius: 25px;
  padding: 40px 55px;
  margin: 60px auto;
  text-align: center;
  font-family: "Inter", sans-serif;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  position: relative;
}

.back-arrow {
  position: absolute;
  top: 25px;
  left: 25px;
  font-size: 20px;
  cursor: pointer;
  transition: transform 0.2s;
}

.back-arrow:hover {
  transform: translateX(-3px);
}

h1 { 
  font-size: 26px; 
  margin-bottom: 15px; 
  color: #1a1a1a;
}

.desc { 
  font-size: 15px; 
  color: #555; 
  line-height: 1.5; 
  margin-bottom: 35px; 
}

.email { 
  font-weight: 600; 
  color: #0044ff;
}

.error-message {
  background: #fee;
  color: #c00;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
  border: 1px solid #fcc;
}

.code-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
}

.code-box {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: #f3f4f6;
  border: 2px solid #ddd;
  font-size: 24px;
  text-align: center;
  font-weight: 600;
  transition: all 0.2s;
}

.code-box:focus {
  outline: none;
  border-color: #0044ff;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(0, 68, 255, 0.1);
}

.code-box:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.resend { 
  color: #555; 
  font-size: 14px; 
  margin-bottom: 25px; 
}

.resend a { 
  color: #0044ff; 
  font-weight: 600; 
  cursor: pointer;
  text-decoration: none;
  transition: opacity 0.2s;
}

.resend a:hover:not(.disabled) { 
  opacity: 0.8;
  text-decoration: underline;
}

.resend a.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn {
  width: 180px;
  padding: 12px 0;
  background: #c8ff32;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: block;
  margin: 15px auto 0 auto;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) { 
  opacity: 0.85;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(200, 255, 50, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.terms {
  margin-top: 25px;
  font-size: 12px;
  color: #777;
  line-height: 1.5;
}

.terms a {
  color: #0044ff;
  font-weight: 600;
  text-decoration: none;
}

.terms a:hover {
  text-decoration: underline;
}
</style>