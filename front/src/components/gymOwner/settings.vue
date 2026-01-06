Asma Lehouche, [04/12/2025 01:56]
<template>
  <div class="settings-page">
    <div class="main-content">
      <!-- Messages d'erreur et de succès -->
      <div v-if="error" class="message error">{{ error }}</div>
      <div v-if="successMessage" class="message success">{{ successMessage }}</div>

      <!-- Personal Information Section -->
      <div class="section-box">
        <h2 class="section-title">Personal Information</h2>

        <div class="form-field">
          <label>Full Name</label>
          <input type="text" v-model="fullName" :disabled="loading" />
        </div>

        <div class="button-row">
          <button class="save-btn" @click="savePersonalInfo" :disabled="loading">
            {{ loading ? "En cours..." : "save changes" }}
          </button>
        </div>
      </div>

      <!-- Change Password Section -->
      <div class="section-box">
        <h2 class="section-title">Change Password</h2>

        <div class="form-field">
          <label>Current password</label>
          <input type="password" v-model="currentPassword" :disabled="loading" />
        </div>

        <div class="form-field">
          <label>New password</label>
          <input type="password" v-model="newPassword" :disabled="loading" />
        </div>

        <div class="form-field">
          <label>Confirm new password</label>
          <input type="password" v-model="confirmPassword" :disabled="loading" />
        </div>

        <div class="button-row">
          <button class="save-btn" @click="changePassword" :disabled="loading">
            {{ loading ? "En cours..." : "Change password" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../../api.js";

const emit = defineEmits(["updateName"]);

const fullName = ref("");
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const displayName = ref("Gym Owner");
const loading = ref(false);
const error = ref("");
const successMessage = ref("");

// Charger le nom complet de l'utilisateur au montage
onMounted(async () => {
  try {
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      fullName.value = user.full_name || "";
      displayName.value = user.full_name || "Gym Owner";
    }
  } catch (e) {
    console.error("Error loading user data:", e);
  }
});

const savePersonalInfo = async () => {
  if (!fullName.value.trim()) {
    error.value = "Le nom complet est requis";
    return;
  }

  loading.value = true;
  error.value = "";
  successMessage.value = "";

  try {
    const response = await api.updateFullName({ full_name: fullName.value.trim() });
    displayName.value = fullName.value;
    emit("updateName", displayName.value);
    
    // Mettre à jour le localStorage
    const userStr = localStorage.getItem('user');
    if (userStr) {
      const user = JSON.parse(userStr);
      user.full_name = fullName.value.trim();
      localStorage.setItem('user', JSON.stringify(user));
    }

    successMessage.value = "Nom mis à jour avec succès";
    setTimeout(() => {
      successMessage.value = "";
    }, 3000);
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data;
      if (typeof data === 'object') {
        error.value = Object.values(data).flat().join(' ');
      } else {
        error.value = data.message || data.error || "Erreur lors de la mise à jour du nom";
      }
    } else {
      error.value = "Erreur lors de la mise à jour du nom";
    }
    console.error("Error updating full name:", err);
  } finally {
    loading.value = false;
  }
};

const changePassword = async () => {
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    error.value = "Veuillez remplir tous les champs";
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    error.value = "Les nouveaux mots de passe ne correspondent pas";
    return;
  }

  if (newPassword.value.length < 8) {
    error.value = "Le nouveau mot de passe doit contenir au moins 8 caractères";
    return;
  }

  loading.value = true;
  error.value = "";
  successMessage.value = "";

  try {
    await api.changePassword({
      old_password: currentPassword.value,
      new_password: newPassword.value,
      confirm_new_password: confirmPassword.value,
    });

    successMessage.value = "Mot de passe changé avec succès";
    currentPassword.value = "";
    newPassword.value = "";
    confirmPassword.value = "";
    
    setTimeout(() => {
      successMessage.value = "";
    }, 3000);
  } catch (err) {
    if (err.response?.data) {
      const data = err.response.data;
      if (typeof data === 'object') {
        // Handle DRF validation errors
        error.value = Object.values(data).flat().join(' ');
      } else {
        error.value = data.message || data.error || "Erreur lors du changement de mot de passe";
      }
    } else {
      error.value = "Erreur lors du changement de mot de passe";
    }
    console.error("Error changing password:", err);
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.settings-page {
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff;
  font-family: "Inter", sans-serif;
}

/* ===== MAIN CONTENT ===== */
.main-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* ===== SECTION BOXES ===== */
.section-box {
  background: #ffffff;
  border: 1px solid #e8e7ec;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 25px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #1f1f1f;
  margin-bottom: 25px;
}

/* ===== FORM FIELDS ===== */
.form-field {
  margin-bottom: 20px;
}

.form-field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.form-field input {
  width: 96%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  font-family: inherit;
  background-color: #f9f9f9;
  transition: 0.2s;
}

.form-field input:focus {
  outline: none;
  border-color: #b3f90f;
  background-color: #ffffff;
}

/* ===== BUTTON ROW ===== */
.button-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 25px;
}

.save-btn {
  background: #b3f90f;
  padding: 12px 40px;
  border-radius: 30px;
  border: none;
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
  transition: 0.2s;
  color: #000;
}

.save-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Messages */
.message {
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.message.error {
  background-color: #fee;
  color: #c33;
  border: 1px solid #fcc;
}

.message.success {
  background-color: #efe;
  color: #3c3;
  border: 1px solid #cfc;
}
</style>
