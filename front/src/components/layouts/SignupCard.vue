<script setup>
import { reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../api'; 

const router = useRouter();
const isLoading = ref(false);
const errorMessage = ref('');
const fileName = ref('');

// Données du formulaire
const form = reactive({
  full_name: '',
  email: '',
  password: '',
  type_utilisateur: 'client',
  nif: '',
  certificat_nif: null
});

// Validation du formulaire
const isFormValid = computed(() => {
  const baseValid = form.full_name.trim() && 
                   form.email.trim() && 
                   form.password.length >= 6;
  
  if (form.type_utilisateur === 'gerant') {
    return baseValid && form.nif.trim() && form.certificat_nif;
  }
  
  return baseValid;
});

// Changer entre User et Gym Owner
const setType = (type) => {
  form.type_utilisateur = type;
  // Réinitialiser les champs spécifiques au gérant
  if (type === 'client') {
    form.nif = '';
    form.certificat_nif = null;
    fileName.value = '';
  }
};

// Gérer l'upload de fichier
const handleFileUpload = (event) => {
  const file = event.target.files[0];
  
  if (file) {
    // Validation du fichier (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      errorMessage.value = "Le fichier ne doit pas dépasser 5MB";
      event.target.value = '';
      return;
    }
    
    // Validation du type de fichier
    const validTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
      errorMessage.value = "Seuls les fichiers PDF et images sont acceptés";
      event.target.value = '';
      return;
    }
    
    form.certificat_nif = file;
    fileName.value = file.name;
    errorMessage.value = '';
  }
};

// Fonction d'inscription
const handleSignup = async () => {
  // Validation
  if (!isFormValid.value) {
    errorMessage.value = "Veuillez remplir tous les champs requis";
    return;
  }
  
  // Validation email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(form.email)) {
    errorMessage.value = "Email invalide";
    return;
  }
  
  errorMessage.value = '';
  isLoading.value = true;

  try {
    let response;
    
    // Si c'est un gérant avec un fichier, on utilise FormData
    if (form.type_utilisateur === 'gerant' && form.certificat_nif) {
      const formData = new FormData();
      formData.append('full_name', form.full_name);
      formData.append('email', form.email);
      formData.append('password', form.password);
      formData.append('type_utilisateur', form.type_utilisateur);
      formData.append('nif', form.nif);
      formData.append('certificat_nif', form.certificat_nif);
      
      response = await api.register(formData, true); // true = FormData
    } else {
      // Pour les clients ou gérants sans fichier, on envoie du JSON
      response = await api.register({
        full_name: form.full_name,
        email: form.email,
        password: form.password,
        type_utilisateur: form.type_utilisateur,
        ...(form.type_utilisateur === 'gerant' && { nif: form.nif })
      });
    }
    
    // Succès : redirection vers VerifyPage
    router.push({ name: 'VerifyPage', query: { email: form.email } });
  
  } catch (error) {
    console.error("Erreur Inscription:", error);
    if (error.response?.data) {
      const data = error.response.data;
      const firstError = Object.values(data).flat()[0];
      errorMessage.value = firstError || "Erreur lors de l'inscription.";
    } else {
      errorMessage.value = "Impossible de contacter le serveur.";
    }
  } finally {
    isLoading.value = false;
  }
};
// ✅ Ajoute cette fonction
const handleGoogleSignup = () => {
  window.location.href = 'http://localhost:8000/api/google-auth/';
};
</script>

<template>
  <div class="signup-card">
    <div class="first-part">
      <h1>Sign Up as</h1>

      <!-- TOGGLE SWITCH -->
      <div class="role-toggle" role="group" aria-label="Type d'utilisateur">
        <button 
          type="button"
          class="role-option"
          :class="{ active: form.type_utilisateur === 'gerant' }" 
          @click="setType('gerant')"
          aria-pressed="form.type_utilisateur === 'gerant'"
        >
          Gym owner
        </button>

        <button 
          type="button"
          class="role-option"
          :class="{ active: form.type_utilisateur === 'client' }" 
          @click="setType('client')"
          aria-pressed="form.type_utilisateur === 'client'"
        >
          User
        </button>
      </div>

      <!-- GOOGLE BUTTON -->
      <div v-if="form.type_utilisateur === 'client'" class="signupWithGoogle">
        <button type="button" class="google-btn" @click="handleGoogleSignup">
  <img 
    src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
    class="google-icon"
    alt="Google logo"
  />
  Sign up with Google
</button>
      </div>
    </div>  

    <div class="middile">
      <p>Or sign up with email</p>
    </div>

    <div class="last-part">
      <form class="signup-form" @submit.prevent="handleSignup">
        <label for="full_name">Full name</label>
        <input 
          id="full_name"
          type="text" 
          placeholder="Full Name" 
          class="input-field" 
          v-model="form.full_name"
          required
        />

        <label for="email">Email address</label>
        <input 
          id="email"
          type="email" 
          placeholder="Email" 
          class="input-field" 
          v-model="form.email"
          required
        />

        <label for="password">Password</label>
        <input 
          id="password"
          type="password" 
          placeholder="Password (min. 6 characters)" 
          class="input-field" 
          v-model="form.password"
          minlength="6"
          required
        />
     
        <!-- Champs spécifiques Gym Owner -->
        <div v-if="form.type_utilisateur === 'gerant'">
          <label for="nif">NIF Code</label>
          <input 
            id="nif"
            type="text" 
            placeholder="Enter NIF code" 
            class="input-field"  
            v-model="form.nif"
            required
          />

          <label for="nif_file">NIF License (upload)</label>
          <label class="file-upload" :class="{ 'has-file': fileName }">
            <span>{{ fileName || 'Select License File' }}</span>
            <input 
              id="nif_file"
              type="file" 
              @change="handleFileUpload"
              accept=".pdf,.jpg,.jpeg,.png"
              required
            />
          </label>
          <p class="file-note">PDF / Image – Max 5MB</p>
        </div>

        <!-- Message d'erreur -->
        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <!-- Bouton de soumission -->
        <button 
          type="submit" 
          :disabled="isLoading || !isFormValid" 
          class="continue-btn"
          :class="{ loading: isLoading }"
        >
          {{ isLoading ? 'Loading...' : 'Continue' }}
        </button>
      </form>

      <p class="ReadyAccount">
        Already have an account? 
        <router-link to="/login">Log in</router-link>
      </p>

      <p class="forgot-password">
        <router-link to="/forgot-password">Forgot password?</router-link>
      </p>

      <p class="terms">
        By clicking 'Continue', you acknowledge that you have read and accept the 
        <a href="#">Terms of Service</a> and <a href="#">Privacy Policy</a>.
      </p>
    </div>  
  </div>
</template>

<style scoped>
/* ---------- File Upload Styling ---------- */
.file-upload {
  width: 96%;
  padding: 12px;
  border: 2px dashed #aab8ff;
  border-radius: 12px;
  background: #f5f7ff;
  text-align: center;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.25s ease;
  display: block;
  margin-top: 8px;
  color: #2d3eff;
}

.file-upload.has-file {
  border-color: #2d3eff;
  background: #e9ecff;
}

.file-upload input[type="file"] {
  display: none;
}

.file-upload:hover {
  background: #e9ecff;
  border-color: #2d3eff;
  transform: scale(1.01);
}

.file-note {
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  text-align: left;
}

/* ----- Error Message ----- */
.error-message {
  color: #ff3b30;
  font-size: 14px;
  text-align: center;
  margin: 15px 0;
  padding: 10px;
  background: #ffebee;
  border-radius: 8px;
  border-left: 3px solid #ff3b30;
}

/* ----- General Card Wrapper ----- */
.signup-card {
  width: 650px;
  max-width: 95%;
  background: #ffffff;
  border-radius: 25px;
  padding: 40px 50px;
  margin: 60px auto;
  box-shadow: 0px 8px 25px rgba(0, 0, 0, 0.12);
  text-align: center;
  font-family: "Inter", sans-serif;
}

/* ----- Title ----- */
.signup-card h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 25px;
  color: #000000;
}

/* ----- Toggle (Gym owner / User) ----- */
.role-toggle {
  display: flex;
  background: #eef2ff;
  padding: 5px;
  border-radius: 30px;
  width: 230px;
  margin: 0 auto 25px;
  gap: 5px;
}

.role-option {
  flex: 1;
  padding: 10px 0;
  border: none;
  background: transparent;
  border-radius: 25px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  color: #333;
  transition: 0.25s ease;
}

.role-option.active {
  background: #0044ff;
  color: white;
  box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}

/* ----- Google Button ----- */
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
  transition: 0.2s;
}

.google-btn:hover {
  background: #f7f7f7;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.google-icon {
  width: 20px;
  height: 20px;
}

/* ----- Divider ----- */
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
  z-index: 1;
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

/* ----- Form ----- */
.signup-form {
  text-align: left;
}

.signup-form label {
  font-size: 14px;
  font-weight: 600;
  margin: 15px 0 5px;
  display: block;
  color: #333;
}

.input-field {
  width: 95%;
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid #e0e0e0;
  background: #f5f5f7;
  margin-bottom: 10px;
  font-size: 14px;
  transition: 0.2s;
}

.input-field:focus {
  outline: none;
  border-color: #0044ff;
  background: white;
}

/* ----- Continue Button ----- */
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
  margin: 15px 0;
  margin-left: auto;
  display: block;
}

.continue-btn:hover:not(:disabled) {
  opacity: 0.8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(200, 255, 50, 0.4);
}

.continue-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.continue-btn.loading {
  position: relative;
  color: transparent;
}

.continue-btn.loading::after {
  content: "";
  position: absolute;
  width: 16px;
  height: 16px;
  top: 50%;
  left: 50%;
  margin-left: -8px;
  margin-top: -8px;
  border: 2px solid #333;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ----- Bottom Text ----- */
.ReadyAccount {
  margin-top: 20px;
  font-size: 14px;
  color: #444;
  text-align: center;
}

.ReadyAccount a {
  color: #0044ff;
  font-weight: 600;
  text-decoration: none;
}

.ReadyAccount a:hover {
  text-decoration: underline;
}

.forgot-password {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}

.forgot-password a {
  color: #0044ff;
  font-weight: 600;
  text-decoration: none;
}

.forgot-password a:hover {
  text-decoration: underline;
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
  text-decoration: none;
}

.terms a:hover {
  text-decoration: underline;
}

/* ----- Responsive ----- */
@media (max-width: 768px) {
  .signup-card {
    padding: 30px 25px;
    margin: 30px auto;
  }
  
  .signup-card h1 {
    font-size: 24px;
  }
}
</style>