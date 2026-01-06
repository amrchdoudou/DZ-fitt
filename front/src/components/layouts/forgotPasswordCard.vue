<template>
  <div class="forgot-card">
    <!-- Back Arrow -->
    <router-link to="/login" class="back-arrow">&#8592;</router-link>

    <!-- Title Section -->
    <div class="first-part">
      <h1>Forgot Password</h1>
      <p class="subtitle">
        Enter your email address below and we'll send you a 4-digit verification code.
      </p>
    </div>

    <!-- Email Form -->
    <div class="last-part">
      <form class="forgot-form" @submit.prevent="sendResetCode">
        <p>Email address</p>
        <input type="email" v-model="email" placeholder="Email" class="input-field" />
        <button type="submit" class="continue-btn">Send Reset Code</button>
      </form>

      <!-- Navigation Links -->
      <p class="switch-page">
        Remembered your password? 
        <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import api from '../../api';

export default {
  name: "ForgotPasswordPage",
  data() {
    return {
      email: "",
      verificationCode: ""
    };
  },
  methods: {
    async sendResetCode() {
  if (!this.email) return alert("Please enter your email.");

  // ✅ Validation email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(this.email)) {
    alert("Invalid email format");
    return;
  }

  try {
    // ✅ Use centralized API
    const response = await api.forgotPassword({ email: this.email });

    console.log("✅ Forgot password success:", response.data);
    alert(`A 4-digit code has been sent to ${this.email}`);
      
    this.$router.push({ 
      path: "/verify", 
      query: { 
        email: this.email,
        from: 'forgot-password'
      }
    });

  } catch (error) {
    console.error("Error:", error);
    const errorMessage = error.response?.data?.error || "Email not found or connection error.";
    alert(errorMessage);
  }
}}
};
</script>

<style scoped>
.forgot-card {
  position: relative; 
  width: 650px;
  background: #ffffff;
  border-radius: 25px;
  padding: 40px 50px;
  margin: 60px auto;
  box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.12);
  font-family: "Inter", sans-serif;
  text-align: left; /* لتجنب ظهور خط فوق السهم */
}

/* Back Arrow */
.back-arrow {
  position: absolute;
  top: 20px;
  left: 20px;
  font-size: 24px;
  cursor: pointer;
  text-decoration: none;
  color: #000;
  user-select: none; /* يمنع تحديد النص عند الضغط */
  line-height: 1;
}

/* Title */
.first-part {
  text-align: center;
}
.first-part h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
  color: #000000;
}
.first-part .subtitle {
  font-size: 14px;
  color: #555;
  margin-bottom: 25px;
}

/* Form */
.forgot-form {
  text-align: left;
}
.forgot-form p {
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
  margin-bottom: 15px;
  font-size: 14px;
}

/* Continue Button */
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
  margin: 15px auto 0 auto; /* مركز أفقيًا */
}
.continue-btn:hover {
  opacity: 0.8;
}

/* Navigation Links */
.switch-page {
  margin-top: 20px;
  font-size: 14px;
  text-align: center;
}
.switch-page a {
  color: #0044ff;
  font-weight: 600;
}
</style>
