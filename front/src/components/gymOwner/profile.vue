<template>
  <div class="page-wrapper">
    <div class="profile-page">
      <!-- TOP BAR -->
      <div class="top-bar">
        <button class="cancel-btn" @click="cancelChanges" :disabled="loading">Cancel</button>
        <button class="save-btn" @click="saveChanges" :disabled="loading">
          {{ loading ? 'Enregistrement...' : 'save changes' }}
        </button>
      </div>
      
      <!-- Messages -->
      <div v-if="successMessage" style="background: #d4edda; color: #155724; padding: 12px; border-radius: 8px; margin: 20px 40px; font-size: 14px; border: 1px solid #c3e6cb;">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" style="background: #fee; color: #c00; padding: 12px; border-radius: 8px; margin: 20px 40px; font-size: 14px; border: 1px solid #fcc;">
        {{ errorMessage }}
      </div>

      <!-- SEPARATOR LINE -->
      <div class="separator-line"></div>

      <!-- MAIN CONTENT -->
      <div class="main-content">
        <!-- TITLE -->
        <h1 class="main-title">Profile</h1>

        <!-- PROFILE COVER -->
        <div class="cover-section">
          <div class="cover-image" :style="coverImageStyle()">
            <input
              type="file"
              ref="coverInput"
              @change="handleCoverUpload"
              accept="image/*"
              style="display: none"
            />
            <!-- SVG button -->
            <button class="edit-cover-btn" @click="$refs.coverInput?.click()">
              <span>✏️</span>
            </button>
          </div>

          <div class="avatar-container">
            <div class="avatar" :style="avatarImageStyle()">
              <input
                type="file"
                ref="avatarInput"
                @change="handleAvatarUpload"
                accept="image/*"
                style="display: none"
              />
            </div>
            <!-- SVG button for avatar -->
            <button class="edit-avatar-btn" @click="$refs.avatarInput?.click()">
              <span>✏️</span>
            </button>
          </div>
        </div>

        <!-- GYM NAME -->
        <div class="field-group">
          <label class="label">Gym name</label>
          <input type="text" v-model="form.name" class="input" />
        </div>

        <!-- PHONE NUMBER -->
        <div class="field-group">
          <label class="label">Phone number</label>
          <input type="tel" v-model="form.phone" class="input" />
        </div>

        <!-- DESCRIPTION -->
        <div class="field-group">
          <label class="label">Description</label>
          <textarea v-model="form.description" class="textarea"></textarea>
        </div>

        <!-- ADDRESS -->
        <h2 class="section-title">Address</h2>
        <div class="card">
          <div class="field-group">
            <label class="label">Country</label>
            <input type="text" v-model="form.country" class="input" :disabled="loading" />
          </div>

          <div class="field-group">
            <label class="label">Wilaya <span style="color: red;">*</span></label>
            <select v-model="form.wilaya" class="select" :disabled="loading" required>
              <option value="" disabled>Select Wilaya</option>
              <option v-for="wilaya in wilayas" :key="wilaya" :value="wilaya">
                {{ wilaya }}
              </option>
            </select>
          </div>

          <div class="field-group">
            <label class="label">City <span style="color: red;">*</span></label>
            <select v-if="availableCities.length > 0" v-model="form.city" class="select" :disabled="loading" required>
              <option value="" disabled>Select City</option>
              <option v-for="city in availableCities" :key="city" :value="city">
                {{ city }}
              </option>
            </select>
            <input v-else type="text" v-model="form.city" class="input" :disabled="loading" required placeholder="Enter City manually" />
          </div>

          <div class="field-group">
            <label class="label">Rue (Street) <span style="color: red;">*</span></label>
            <input type="text" v-model="form.rue" class="input" :disabled="loading" required placeholder="e.g. 12 Rue Didouche Mourad" />
            <small style="color: #666; display: block; margin-top: 4px;">Enter the exact street name and number for better geocoding results.</small>
          </div>

          <div class="field-group">
            <label class="label">code/Postal</label>
            <input type="text" v-model="form.codePostal" class="input" :disabled="loading" />
          </div>

          <!-- Geocoding Status -->
          <div class="field-group" v-if="form.latitude && form.longitude">
            <label class="label">Position (Geocoded)</label>
            <div class="geo-status success">
              <span class="geo-icon">📍</span>
              <a 
                :href="`https://www.google.com/maps?q=${form.latitude},${form.longitude}`" 
                target="_blank" 
                class="geo-link"
              >
                Voir sur Google Maps
              </a>
            </div>
          </div>
          <div class="field-group" v-else-if="!isCreatingNew">
            <label class="label">Position</label>
            <div class="geo-status warning">
              <span class="geo-icon">⚠️</span>
              <span>Running geocoding... (Save to update)</span>
            </div>
          </div>
        </div>

        <!-- GALERIE -->
        <h2 class="section-title">Galerie</h2>
        <div class="gallery">
          <div
            v-for="(item, index) in galleryImages"
            :key="'img-' + index"
            class="gallery-item"
            :style="{ backgroundImage: item.url ? `url(${item.url})` : 'none' }"
          >
            <button class="remove-gallery-btn" @click="removeGalleryImage(index)">
              ✕
            </button>
          </div>
          <div class="gallery-upload" @click="$refs.galleryInput?.click()">
            <input
              type="file"
              ref="galleryInput"
              @change="handleGalleryUpload"
              accept="image/*"
              multiple
              style="display: none"
            />
            <span class="gallery-icon">📷</span>
            <span class="upload-text">Drag & drop or browse files</span>
          </div>
        </div>

        <!-- SUBSCRIPTION PLANS -->
        <div class="plan-header">
          <h2 class="section-title">Subscription plans</h2>
          <button class="add-circle-btn" @click="addPlan">+</button>
        </div>

        <div v-for="(plan, index) in form.plans" :key="index" class="plan-card">
          <div class="plan-row">
            <div class="plan-field">
              <label class="label">Plan name</label>
              <input type="text" v-model="plan.name" class="input" :disabled="loading" />
            </div>

            <div class="plan-field">
              <label class="label">Price</label>
              <input type="number" v-model="plan.price" class="input" :disabled="loading" />
            </div>

            <div class="plan-field">
              <label class="label">Sessions/Month</label>
              <input type="number" v-model="plan.sessions" class="input" :disabled="loading" placeholder="e.g. 12" min="1" />
            </div>

            <div class="plan-field">
              <label class="label">Per</label>
              <select v-model="plan.per" class="select" :disabled="loading">
                <option>month</option>
                <option>session</option>
              </select>
            </div>

            <div class="plan-field">
              <label class="label">Color</label>
              <select v-model="plan.color" class="select" :disabled="loading">
                <option>green</option>
                <option>white</option>
                <option>red</option>
              </select>
            </div>

            <button class="remove-btn" @click="removePlan(index)" :disabled="loading">✕</button>
          </div>
        </div>

        <!-- Equipments -->
        <h2 class="section-title">Equipments</h2>
        <div class="card checkbox-list">
          <label 
            v-for="equip in availableEquipements" 
            :key="equip.id"
            class="checkbox-label"
          >
            <input 
              type="checkbox" 
              :value="equip.id"
              v-model="selectedEquipements"
              :disabled="loading"
            />
            <span>{{ equip.name }}</span>
          </label>
        </div>

        <!-- SERVICES -->
        <h2 class="section-title">Services</h2>
        <div class="card checkbox-list">
          <label 
            v-for="service in availableServices" 
            :key="service.id"
            class="checkbox-label"
          >
            <input 
              type="checkbox" 
              :value="service.id"
              v-model="selectedServices"
              :disabled="loading"
            />
            <span>{{ service.label || service.nom }}</span>
          </label>
        </div>

        <!-- OPENING HOURS -->
        <h2 class="section-title">Opening hours</h2>
        <div v-for="(day, index) in days" :key="day.name" class="hours-card">
          <label class="day-checkbox">
            <input type="checkbox" v-model="day.enabled" :disabled="loading" />
            <span class="day-name">{{ day.name }}</span>
          </label>
          <input type="time" v-model="day.open" class="time-input" :disabled="loading || !day.enabled" />
          <input type="time" v-model="day.close" class="time-input" :disabled="loading || !day.enabled" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import api from "../../api";
import { algeriaWilayas, algeriaCities } from "../../data/algeria";

export default {
  props: {
    isCreatingNewSalle: Boolean,
    initialSalleId: Number,
    selectedGymId: [Number, String], // ID of the currently selected gym from sidebar or 'new'
  },
  emits: ['updateSalleId', 'updateIsCreatingNewSalle', 'gymSaved'],
  setup(props, { emit }) {
    // Expose wilayas to template
    const wilayas = algeriaWilayas;
    const availableCities = ref([]);

    const salleId = ref(null);
    const loading = ref(false);
    const errorMessage = ref("");
    const successMessage = ref("");
    
    // Images
    const coverImage = ref(null);
    const coverImageFile = ref(null);
    const avatarImage = ref(null);
    const avatarImageFile = ref(null);
    const galleryImages = ref([]); // Array of {url, id, file}
    
    // Form data
    const form = ref({
      name: "",
      phone: "",
      description: "",
      country: "Algérie",
      wilaya: "",
      city: "",
      rue: "",
      codePostal: "",
      plans: [],
    });
    
    // Available options from backend
    const availableEquipements = ref([]);
    const availableServices = ref([]);
    const selectedEquipements = ref([]); // Array of equipment IDs
    const selectedServices = ref([]); // Array of service IDs
    
    // Days mapping
    const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    const dayMapping = {
      'Monday': 'monday',
      'Tuesday': 'tuesday',
      'Wednesday': 'wednesday',
      'Thursday': 'thursday',
      'Friday': 'friday',
      'Saturday': 'saturday',
      'Sunday': 'sunday',
    };
    
    const days = ref([
      { name: "Monday", value: "monday", open: "", close: "", enabled: false },
      { name: "Tuesday", value: "tuesday", open: "", close: "", enabled: false },
      { name: "Wednesday", value: "wednesday", open: "", close: "", enabled: false },
      { name: "Thursday", value: "thursday", open: "", close: "", enabled: false },
      { name: "Friday", value: "friday", open: "", close: "", enabled: false },
      { name: "Saturday", value: "saturday", open: "", close: "", enabled: false },
      { name: "Sunday", value: "sunday", open: "", close: "", enabled: false },
    ]);
    
    const isCreatingNew = ref(false);

    // Watcher for Wilaya to update Cities
    watch(() => form.value.wilaya, (newWilaya) => {
      console.log("Wilaya changed to:", newWilaya);
      if (newWilaya) {
        // Find the wilaya case-insensitively
        const wilayaKey = Object.keys(algeriaCities).find(
          key => key.toLowerCase() === newWilaya.toLowerCase()
        );
        
        if (wilayaKey && algeriaCities[wilayaKey]) {
          console.log("Found cities for:", newWilaya, algeriaCities[wilayaKey]);
          availableCities.value = algeriaCities[wilayaKey];
          // If current city is not in new list, clear it
          if (form.value.city && !availableCities.value.includes(form.value.city)) {
            form.value.city = "";
          }
        } else {
          console.log("No cities found for:", newWilaya);
          availableCities.value = [];
          if (availableCities.value.length === 0 && newWilaya) {
             availableCities.value = [newWilaya]; // Default to Chef-lieu
          }
        }
      }
    });
    
    // Load initial data
    const loadData = async () => {
      console.log("🔄 loadData called");
      console.log("Props:", { 
        selectedGymId: props.selectedGymId, 
        initialSalleId: props.initialSalleId,
        isCreatingNewSalle: props.isCreatingNewSalle 
      });
      
      loading.value = true;
      errorMessage.value = "";
      
      // Check if we're in create mode from props
      // Only enter create mode if explicitly requested AND no gym is selected
      if (props.isCreatingNewSalle && !props.selectedGymId) {
        console.log("📝 Create mode detected");
        isCreatingNew.value = true;
        salleId.value = null;
        form.value = {
          name: "",
          phone: "",
          description: "",
          country: "Algérie",
          wilaya: "",
          city: "",
          rue: "",
          codePostal: "",
          plans: [{ name: "", price: "", sessions: 1, per: "month", color: "green" }],
        };
        coverImage.value = null;
        coverImageFile.value = null;
        avatarImage.value = null;
        avatarImageFile.value = null;
        galleryImages.value = [];
        selectedEquipements.value = [];
        selectedServices.value = [];
        days.value.forEach(day => { day.enabled = false; day.open = ""; day.close = ""; });
        // Load available equipements and services even when creating new salle
        await loadEquipements();
        await loadServices();
        loading.value = false;
        return;
      }
      
      isCreatingNew.value = false;
      
      try {
        // If we just created a salle, salleId.value will be set.
        // We should use it even if props.selectedGymId is still 'new' (until parent updates it)
        if (salleId.value && salleId.value !== 'new') {
           isCreatingNew.value = false;
           console.log("📍 Using local salleId:", salleId.value);
        } else if (props.selectedGymId === 'new') {
           console.log("✨ Creating new gym (forced by 'new' ID)");
           isCreatingNew.value = true;
           salleId.value = null;
           form.value = {
             name: "",
             phone: "",
             description: "",
             country: "Algérie",
             wilaya: "",
             city: "",
             rue: "",
             codePostal: "",
             plans: [{ name: "", price: "", sessions: 1, per: "month", color: "green" }],
           };
           coverImage.value = null;
           coverImageFile.value = null;
           avatarImage.value = null;
           avatarImageFile.value = null;
           galleryImages.value = [];
           selectedEquipements.value = [];
           selectedServices.value = [];
           days.value.forEach(day => { day.enabled = false; day.open = ""; day.close = ""; });
           await loadEquipements();
           await loadServices();
           loading.value = false;
           return;
        }

        if (!salleId.value) {
          if (props.selectedGymId && props.selectedGymId !== 'new') {
            console.log("✅ Using selectedGymId:", props.selectedGymId);
            salleId.value = props.selectedGymId;
          } else if (props.initialSalleId) {
            salleId.value = props.initialSalleId;
          } else {
            // Fallback: Get gérant's salles and use first one
            const sallesResponse = await api.getMySalles();
            if (sallesResponse.data.length === 0) {
              // No salle exists, show create form
              isCreatingNew.value = true;
              salleId.value = null;
              form.value = {
                name: "",
                phone: "",
                description: "",
                country: "Algérie",
                wilaya: "",
                city: "",
                rue: "",
                codePostal: "",
                plans: [{ name: "", price: "", sessions: 1, per: "month", color: "green" }],
              };
              coverImage.value = null;
              coverImageFile.value = null;
              avatarImage.value = null;
              avatarImageFile.value = null;
              galleryImages.value = [];
              selectedEquipements.value = [];
              selectedServices.value = [];
              days.value.forEach(day => { day.enabled = false; day.open = ""; day.close = ""; });
              // Load available equipements and services even when creating new salle
              await loadEquipements();
              await loadServices();
              loading.value = false;
              return;
            }
            salleId.value = sallesResponse.data[0].id;
          }
        }
        
        console.log("📍 Loading data for salle ID:", salleId.value);
        
        // 2. Load salle details
        const salleResponse = await api.getSalleDetail(salleId.value);
        const salle = salleResponse.data;
        
        console.log("📦 Salle data loaded:", salle);
        
        // Map salle data to form
        form.value = {
          name: salle.nom || "",
          phone: salle.telephone || "",
          description: salle.description || "",
          country: salle.pays || "Algérie",
          wilaya: salle.wilaya || "",
          city: salle.ville || "",
          rue: salle.rue || "",
          codePostal: salle.codePostal || "",
          latitude: salle.latitude,
          longitude: salle.longitude,
          plans: [],
        };
        
        // Manually populate availableCities based on loaded wilaya
        if (form.value.wilaya) {
          // Find the wilaya case-insensitively
          const wilayaKey = Object.keys(algeriaCities).find(
            key => key.toLowerCase() === form.value.wilaya.toLowerCase()
          );
          
          if (wilayaKey && algeriaCities[wilayaKey]) {
            availableCities.value = algeriaCities[wilayaKey];
            console.log("🏙️ Cities populated for", form.value.wilaya, ":", availableCities.value.length, "cities");
          } else {
            console.log("⚠️ No cities found for wilaya:", form.value.wilaya);
            availableCities.value = [];
          }
        }
        
        console.log("📝 Form populated:", form.value);
        
        // 3. Load photos
        await loadPhotos();
        
        // 4. Load formules (plans)
        await loadFormules();
        
        // 5. Load equipements (always load available list, even if no salle)
        await loadEquipements();
        
        // 6. Load services (always load available list, even if no salle)
        await loadServices();
        
        // 7. Load schedules (opening hours)
        await loadSchedules();
        
      } catch (error) {
        console.error("❌ Error loading data:", error);
        console.error("Error details:", error.response?.data);
        errorMessage.value = "Erreur lors du chargement des données: " + (error.response?.data?.detail || error.message);
      } finally {
        loading.value = false;
      }
    };
    
    const loadPhotos = async () => {
      try {
        console.log("📸 Loading photos for salle:", salleId.value);
        const response = await api.getSallePhotos(salleId.value);
        const photos = response.data;
        
        console.log("📸 Photos received:", photos);
        console.log("📸 Number of photos:", photos.length);
        
        // Find cover and profile photos
        const coverPhoto = photos.find(p => p.photo_type === 'cover');
        const profilePhoto = photos.find(p => p.photo_type === 'profile');
        const galleryPhotos = photos.filter(p => p.photo_type === 'gallery');
        
        console.log("📸 Cover photo:", coverPhoto);
        console.log("📸 Profile photo:", profilePhoto);
        console.log("📸 Gallery photos count:", galleryPhotos.length);
        
        if (coverPhoto) {
          coverImage.value = coverPhoto.image_url || coverPhoto.image;
          console.log("✅ Cover image URL:", coverImage.value);
        }
        if (profilePhoto) {
          avatarImage.value = profilePhoto.image_url || profilePhoto.image;
          console.log("✅ Avatar image URL:", avatarImage.value);
        }
        galleryImages.value = galleryPhotos.map(p => ({ 
          url: p.image_url || p.image, 
          id: p.id, 
          file: null 
        }));
        console.log("✅ Gallery images:", galleryImages.value);
      } catch (error) {
        console.error("❌ Error loading photos:", error);
      }
    };
    
    const loadFormules = async () => {
      try {
        const response = await api.getFormules(salleId.value);
        form.value.plans = response.data.map(f => ({
          id: f.id,
          name: f.nom || "",
          price: f.prix_mensuel ? parseFloat(f.prix_mensuel) : "",
          sessions: f.number_science || 1,
          per: "month", // Backend only has prix_mensuel
          color: "green",
        }));
        
        if (form.value.plans.length === 0) {
          form.value.plans = [{ name: "", price: "", sessions: 1, per: "month", color: "green" }];
        }
      } catch (error) {
        console.error("Error loading formules:", error);
        form.value.plans = [{ name: "", price: "", per: "month", color: "green" }];
      }
    };
    
    const loadEquipements = async () => {
      try {
        console.log("📦 Loading equipements...");
        // Load all available equipements from backend
        const allResponse = await api.getAllEquipements();
        console.log("📦 Equipements response:", allResponse.data);
        availableEquipements.value = allResponse.data || [];
        
        if (availableEquipements.value.length === 0) {
          console.warn("⚠️ Aucun équipement disponible dans la base de données. Veuillez en créer via l'admin Django.");
        }
        
        // Load salle's equipements if salle exists
        if (salleId.value) {
          try {
            const salleResponse = await api.getSalleEquipements(salleId.value);
            console.log("📦 Salle equipements:", salleResponse.data);
            // Extract equipement_id from SalleEquipement objects
            selectedEquipements.value = salleResponse.data.map(e => {
              // SalleEquipementSerializer returns {id, equipement, equipement_id}
              // equipement_id is returned by get_equipement_id method
              return e.equipement_id || (e.equipement && typeof e.equipement === 'object' ? e.equipement.id : e.equipement) || e.id;
            }).filter(id => id != null);
          } catch (err) {
            console.warn("No equipements found for salle:", err);
            selectedEquipements.value = [];
          }
        } else {
          selectedEquipements.value = [];
        }
      } catch (error) {
        console.error("❌ Error loading equipements:", error);
        console.error("❌ Error details:", error.response?.data || error.message);
        availableEquipements.value = [];
        selectedEquipements.value = [];
        // Show user-friendly error
        errorMessage.value = "Erreur lors du chargement des équipements: " + (error.response?.data?.detail || error.message);
      }
    };
    
    const loadServices = async () => {
      try {
        console.log("🔧 Loading services...");
        // Load all available services from backend
        const allResponse = await api.getAllServices();
        console.log("🔧 Services response:", allResponse.data);
        availableServices.value = allResponse.data || [];
        
        if (availableServices.value.length === 0) {
          console.warn("⚠️ Aucun service disponible dans la base de données. Veuillez en créer via l'admin Django.");
        }
        
        // Load salle's services if salle exists
        if (salleId.value) {
          try {
            const salleResponse = await api.getSalleServices(salleId.value);
            console.log("🔧 Salle services:", salleResponse.data);
            // Extract service ID from SalleService objects
            // SalleServiceSerializer returns {id, service, service_info, date_ajout}
            // 'service' is the ID of the Service
            selectedServices.value = salleResponse.data.map(s => {
              // service can be an ID or an object
              const serviceId = typeof s.service === 'object' ? s.service.id : s.service;
              return serviceId || s.service_id || s.id;
            }).filter(id => id != null);
          } catch (err) {
            console.warn("No services found for salle:", err);
            selectedServices.value = [];
          }
        } else {
          selectedServices.value = [];
        }
      } catch (error) {
        console.error("❌ Error loading services:", error);
        console.error("❌ Error details:", error.response?.data || error.message);
        availableServices.value = [];
        selectedServices.value = [];
        // Show user-friendly error
        errorMessage.value = "Erreur lors du chargement des services: " + (error.response?.data?.detail || error.message);
      }
    };
    
    const loadSchedules = async () => {
      try {
        const response = await api.getSalleHoraires(salleId.value);
        const schedules = response.data;
        
        // Define mapping from backend Day keys (e.g. "LUNDI") to our values ("monday")
        const reverseDayMapping = {
          'LUNDI': 'monday',
          'MARDI': 'tuesday',
          'MERCREDI': 'wednesday',
          'JEUDI': 'thursday',
          'VENDREDI': 'friday',
          'SAMEDI': 'saturday',
          'DIMANCHE': 'sunday',
        };

        days.value.forEach(day => {
          // Find matching schedule - keys might be LUNDI etc.
          const schedule = schedules.find(s => reverseDayMapping[s.jourSemaine] === day.value);
          
          if (schedule) {
            day.enabled = !schedule.estFerme;
            // Extract time (HH:MM)
            day.open = schedule.heureOuverture ? schedule.heureOuverture.substring(0, 5) : "";
            day.close = schedule.heureFermeture ? schedule.heureFermeture.substring(0, 5) : "";
          } else {
            day.enabled = false;
            day.open = "";
            day.close = "";
          }
        });
      } catch (error) {
        console.error("Error loading schedules:", error);
      }
    };
    
    // Photo handlers
    const handleCoverUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        coverImageFile.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          coverImage.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };
    
    const handleAvatarUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        avatarImageFile.value = file;
        const reader = new FileReader();
        reader.onload = (e) => {
          avatarImage.value = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    };
    
    const handleGalleryUpload = (event) => {
      const files = Array.from(event.target.files);
      files.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          galleryImages.value.push({ url: e.target.result, id: null, file: file });
        };
        reader.readAsDataURL(file);
      });
      event.target.value = "";
    };
    
    const removeGalleryImage = (index) => {
      const item = galleryImages.value[index];
      // If it has an ID, mark for deletion (we'll delete it on save)
      galleryImages.value.splice(index, 1);
    };
    
    // Plan handlers
    const addPlan = () => {
      form.value.plans.push({ 
        name: "", 
        price: "", 
        sessions: 1,
        per: "month", 
        color: "green" 
      });
    };
    
    const removePlan = (index) => {
      form.value.plans.splice(index, 1);
    };
    
    // Save all data
    // Save all data
    const saveChanges = async () => {
      console.log("📝 Attempting to save...");
      console.log("Current Form State:", JSON.parse(JSON.stringify(form.value)));
      
      loading.value = true;
      errorMessage.value = "";
      successMessage.value = "";
      
      try {
        // If creating new salle
        if (isCreatingNew.value || (!salleId.value && !props.initialSalleId)) {
          console.log("🏗️ Creating new salle...");
          
          
          // Validate required fields (trim whitespace)
          const name = (form.value.name || "").trim();
          const city = (form.value.city || "").trim();
          const wilaya = (form.value.wilaya || "").trim();
          const rue = (form.value.rue || "").trim();
          
          console.log("Validation:", { name, city, wilaya, rue });
          
          if (!name || name.length === 0) {
            errorMessage.value = "Le nom de la salle est obligatoire.";
            loading.value = false;
            return;
          }
          
          if (!city || city.length === 0) {
            errorMessage.value = "La ville est obligatoire.";
            loading.value = false;
            return;
          }
          
          if (!wilaya || wilaya.length === 0) {
            errorMessage.value = "La wilaya est obligatoire.";
            loading.value = false;
            return;
          }
          
          if (!rue || rue.length === 0) {
            errorMessage.value = "La rue est obligatoire.";
            loading.value = false;
            return;
          }
          
          // Create new salle
          const newSalleData = {
            nom: name,
            telephone: (form.value.phone || "").trim(),
            description: (form.value.description || "").trim(),
            pays: form.value.country || "Algérie",
            wilaya: wilaya,
            ville: city,
            rue: rue,
            codePostal: (form.value.codePostal || "").trim(),
            codePostal: (form.value.codePostal || "").trim(),
            // Pass null to let backend handle geocoding or defaults
            latitude: null, 
            longitude: null,
          };
          
          console.log("📤 Sending create request:", newSalleData);
          const createResponse = await api.createSalle(newSalleData);
          console.log("✅ Salle created:", createResponse.data);
          
          const newSalleId = createResponse.data.id;
          salleId.value = newSalleId;
          isCreatingNew.value = false;
          
          // Persist selection immediately
          localStorage.setItem('selectedGymId', newSalleId);
          
          // Emit events to parent
          emit('updateSalleId', newSalleId);
          emit('updateIsCreatingNewSalle', false);
          emit('gymSaved', newSalleId); // Pass the new gym ID
          
          successMessage.value = "Salle créée avec succès !";
          
          // Now save equipements and services if any were selected
          if (selectedEquipements.value.length > 0) {
            console.log("📦 Adding equipements:", selectedEquipements.value);
            for (const equipId of selectedEquipements.value) {
              try {
                await api.addSalleEquipement(newSalleId, { equipement_write: equipId });
              } catch (e) {
                console.error("Error adding equipement:", e);
              }
            }
          }
          
          if (selectedServices.value.length > 0) {
            console.log("🔧 Adding services:", selectedServices.value);
            for (const serviceId of selectedServices.value) {
              try {
                await api.addSalleService(newSalleId, serviceId);
              } catch (e) {
                console.error("Error adding service:", e);
              }
            }
          }
          
          // Save formules (plans) if any
          if (form.value.plans && form.value.plans.length > 0) {
            console.log("💳 Adding formules:", form.value.plans);
            for (const plan of form.value.plans) {
              if (plan.name && plan.price) {
                try {
                  await api.createFormule(newSalleId, {
                    salle: newSalleId,
                    nom: plan.name,
                    prix_mensuel: parseFloat(plan.price) || 0,
                    number_science: plan.sessions || 1,
                  });
                } catch (e) {
                  console.error("Error adding formule:", e);
                }
              }
            }
          }
          
          // Upload photos if any
          if (coverImageFile.value) {
            try {
              const formData = new FormData();
              formData.append('image', coverImageFile.value);
              formData.append('photo_type', 'cover');
              await api.addSallePhoto(newSalleId, formData);
            } catch (e) {
              console.error("Error adding cover photo:", e);
            }
          }
          
          if (avatarImageFile.value) {
            try {
              const formData = new FormData();
              formData.append('image', avatarImageFile.value);
              formData.append('photo_type', 'profile');
              await api.addSallePhoto(newSalleId, formData);
            } catch (e) {
              console.error("Error adding profile photo:", e);
            }
          }
          
          // Upload gallery photos
          for (const item of galleryImages.value) {
            if (item.file) {
              try {
                const formData = new FormData();
                formData.append('image', item.file);
                formData.append('photo_type', 'gallery');
                await api.addSallePhoto(newSalleId, formData);
              } catch (e) {
                console.error("Error adding gallery photo:", e);
              }
            }
          }
          
          // Sauvegarder les horaires pour la nouvelle salle
          const dayMappingHoraires = {
            'monday': 'LUNDI',
            'tuesday': 'MARDI',
            'wednesday': 'MERCREDI',
            'thursday': 'JEUDI',
            'friday': 'VENDREDI',
            'saturday': 'SAMEDI',
            'sunday': 'DIMANCHE',
          };

          const initialHoraires = days.value.map(day => {
            if (day.enabled && day.open && day.close) {
              return {
                jourSemaine: dayMappingHoraires[day.value],
                heureOuverture: day.open,
                heureFermeture: day.close,
                estFerme: false
              };
            } else {
              return {
                jourSemaine: dayMappingHoraires[day.value],
                estFerme: true,
                heureOuverture: null,
                heureFermeture: null
              };
            }
          });
          
          try {
            console.log("⏰ Saving initial opening hours:", initialHoraires);
            await api.updateSalleHoraires(newSalleId, initialHoraires);
          } catch (e) {
            console.error("Error adding horaires during creation:", e);
          }

          // Reload all data to show the created salle
          console.log("🔄 Reloading data for salle:", newSalleId);
          // Force load with the new salle ID by updating props state
          await loadData();
          loading.value = false;
          return;
        }
        
        console.log("📝 Updating salle ID:", salleId.value);
        console.log("📝 Update data:", {
          nom: form.value.name,
          telephone: form.value.phone,
          wilaya: form.value.wilaya,
          ville: form.value.city
        });
        
        const updatePayload = {
          nom: form.value.name,
          telephone: form.value.phone,
          description: form.value.description,
          pays: form.value.country,
          wilaya: form.value.wilaya,
          ville: form.value.city,
          rue: form.value.rue,
          codePostal: form.value.codePostal,
        };
        
        console.log("📤 Full payload being sent:", JSON.stringify(updatePayload, null, 2));
        console.log("📤 Wilaya type:", typeof updatePayload.wilaya);
        console.log("📤 Wilaya value:", updatePayload.wilaya);
        
        // 1. Update salle basic info
        await api.updateSalle(salleId.value, updatePayload);
        
        // 2. Upload cover photo if changed
        if (coverImageFile.value) {
          const formData = new FormData();
          formData.append('image', coverImageFile.value);
          formData.append('photo_type', 'cover');
          await api.addSallePhoto(salleId.value, formData);
        }
        
        // 3. Upload avatar photo if changed
        if (avatarImageFile.value) {
          const formData = new FormData();
          formData.append('image', avatarImageFile.value);
          formData.append('photo_type', 'profile');
          await api.addSallePhoto(salleId.value, formData);
        }
        
        // 4. Upload new gallery photos
        for (const item of galleryImages.value) {
          if (item.file && !item.id) {
            const formData = new FormData();
            formData.append('image', item.file);
            formData.append('photo_type', 'gallery');
            await api.addSallePhoto(salleId.value, formData);
          }
        }
        
        // 5. Update formules (plans)
        const currentFormules = await api.getFormules(salleId.value);
        const currentIds = currentFormules.data.map(f => f.id);
        
        // Delete removed plans
        for (const formule of currentFormules.data) {
          if (!form.value.plans.find(p => p.id === formule.id)) {
            await api.deleteFormule(salleId.value, formule.id);
          }
        }
        
        // Create/update plans
        for (const plan of form.value.plans) {
          if (plan.id) {
            // Update existing
            await api.updateFormule(salleId.value, plan.id, {
              salle: salleId.value,
              nom: plan.name,
              prix_mensuel: parseFloat(plan.price) || 0,
              number_science: plan.sessions || 1, // Number of sessions per month
            });
          } else if (plan.name) {
            // Create new
            await api.createFormule(salleId.value, {
              salle: salleId.value,
              nom: plan.name,
              prix_mensuel: parseFloat(plan.price) || 0,
              number_science: plan.sessions || 1,
            });
          }
        }
        
        // 6. Update equipements
        try {
          const currentEquipements = await api.getSalleEquipements(salleId.value);
          // Extract equipement_id correctly (now backend includes it)
          const currentEquipIds = currentEquipements.data.map(e => {
            return e.equipement_id || (e.equipement && typeof e.equipement === 'object' ? e.equipement.id : e.equipement) || e.id;
          }).filter(id => id != null);
          
          // Remove unselected
          for (const equipId of currentEquipIds) {
            if (!selectedEquipements.value.includes(equipId)) {
              await api.deleteSalleEquipement(salleId.value, equipId);
            }
          }
          
          // Add new (only IDs that are in selected but not in current)
          for (const equipId of selectedEquipements.value) {
            if (!currentEquipIds.includes(equipId)) {
              await api.addSalleEquipement(salleId.value, { equipement_write: equipId });
            }
          }
        } catch (err) {
          console.warn("Error updating equipements:", err);
          // If no equipements exist yet, just add selected ones
          for (const equipId of selectedEquipements.value) {
            try {
              await api.addSalleEquipement(salleId.value, { equipement_write: equipId });
            } catch (e) {
              console.error("Error adding equipement:", e);
            }
          }
        }
        
        // 7. Update services
        try {
          const currentServices = await api.getSalleServices(salleId.value);
          // Extract service ID correctly
          const currentServiceIds = currentServices.data.map(s => {
            const serviceId = typeof s.service === 'object' ? s.service.id : s.service;
            return serviceId || s.service_id || s.id;
          }).filter(id => id != null);
          
          // Remove unselected
          for (const serviceId of currentServiceIds) {
            if (!selectedServices.value.includes(serviceId)) {
              await api.deleteSalleService(salleId.value, serviceId);
            }
          }
          
          // Add new (only IDs that are in selected but not in current)
          for (const serviceId of selectedServices.value) {
            if (!currentServiceIds.includes(serviceId)) {
              await api.addSalleService(salleId.value, serviceId);
            }
          }
        } catch (err) {
          console.warn("Error updating services:", err);
          // If no services exist yet, just add selected ones
          for (const serviceId of selectedServices.value) {
            try {
              await api.addSalleService(salleId.value, serviceId);
            } catch (e) {
              console.error("Error adding service:", e);
            }
          }
        }
        
        // 8. Update schedules (opening hours)
        const dayMapping = {
          'monday': 'LUNDI',
          'tuesday': 'MARDI',
          'wednesday': 'MERCREDI',
          'thursday': 'JEUDI',
          'friday': 'VENDREDI',
          'saturday': 'SAMEDI',
          'sunday': 'DIMANCHE',
        };

        const horairesData = [];
        
        for (const day of days.value) {
            if (day.enabled && day.open && day.close) {
                horairesData.push({
                    jourSemaine: dayMapping[day.value],
                    heureOuverture: day.open,
                    heureFermeture: day.close,
                    estFerme: false
                });
            }
        }
        
        await api.updateSalleHoraires(salleId.value, horairesData);
        
        successMessage.value = "Modifications enregistrées avec succès!";
        
        // Emit event to parent to refresh sidebar gym list
        emit('gymSaved');
        
        // Reload data to get updated photos URLs
        await loadData();
        
      } catch (error) {
        console.error("Error saving:", error);
        
        let msg = "Une erreur est survenue lors de l'enregistrement.";
        
        if (error.response) {
            console.error("Backend Error Data:", error.response.data);
            console.error("Backend Error Status:", error.response.status);
            
            if (error.response.data) {
                const data = error.response.data;
                
                // If detailed validation errors (Django DRF format)
                if (typeof data === 'object' && !Array.isArray(data)) {
                    const messages = Object.entries(data).map(([key, value]) => {
                        const valStr = Array.isArray(value) ? value.join(", ") : String(value);
                        return `${key}: ${valStr}`;
                    });
                    if (messages.length > 0) {
                        msg = "Erreur de validation : " + messages.join(" | ");
                    }
                } else if (data.detail) {
                    msg = data.detail;
                } else {
                    msg = "Erreur : " + JSON.stringify(data);
                }
            }
        } else {
            msg = error.message;
        }
        
        errorMessage.value = msg;
      } finally {
        loading.value = false;
      }
    };
    
    const cancelChanges = () => {
      loadData();
    };
    
    // Computed properties
    const coverImageStyle = () => {
      return coverImage.value ? {
        backgroundImage: `url(${coverImage.value})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      } : {};
    };
    
    const avatarImageStyle = () => {
      return avatarImage.value ? {
        backgroundImage: `url(${avatarImage.value})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      } : {};
    };
    
    onMounted(() => {
      loadData();
    });

    watch(() => props.initialSalleId, (newId) => {
      if (newId !== salleId.value) {
        loadData();
      }
    });
    
    watch(() => props.isCreatingNewSalle, (newVal) => {
      if (newVal !== isCreatingNew.value) {
        loadData();
      }
    });
    
    return {
      salleId,
      loading,
      errorMessage,
      successMessage,
      coverImage,
      coverImageFile,
      avatarImage,
      avatarImageFile,
      galleryImages,
      form,
      availableEquipements,
      availableServices,
      selectedEquipements,
      selectedServices,
      days,
      loadData,
      handleCoverUpload,
      handleAvatarUpload,
      handleGalleryUpload,
      removeGalleryImage,
      wilayas, 
      availableCities,
      addPlan,
      removePlan,
      saveChanges,
      cancelChanges,
      coverImageStyle,
      avatarImageStyle,
    };
  },

};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.page-wrapper {
  background: #fff;
  min-height: 100vh;
}

.container {
  background: #fff;
  min-height: 100vh;
  padding: 20px;
}

.profile-page {
  max-width: 100%;
  margin: auto;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* TOP BAR */
.top-bar {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 40px;
  background: #fff;
}

/* SEPARATOR LINE */
.separator-line {
  width: 100%;
  height: 1px;
  background: #e0e0e0;
  margin-bottom: 30px;
}

/* MAIN CONTENT */
.main-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 40px 40px 40px;
}

.save-btn,
.cancel-btn {
  padding: 0 40px;
  height: 44px;
  border-radius: 30px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 600;
  transition: 0.2s;
}

.save-btn {
  background: #b3f90f;
  color: #000;
}

.save-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.cancel-btn {
  background: #fff;
  border: 1px solid #ff4444;
  color: #ff4444;
}

.cancel-btn:hover {
  background: #fff5f5;
}

/* TITLE */
.main-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 20px;
}

/* COVER */
.cover-section {
  position: relative;
  margin-bottom: 70px;
  background: #fff;
  padding: 20px;
  border-radius: 16px;
}

.cover-image {
  height: 160px;
  background: #333;
  border-radius: 16px;
  position: relative;
}

.edit-cover-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  background: #b3f90f;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  transition: 0.2s;
}

.edit-cover-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.avatar-container {
  position: absolute;
  bottom: -50px;
  left: 40px;
}

.avatar {
  width: 100px;
  height: 100px;
  background: #000;
  border-radius: 50%;
  border: 4px solid #fff;
}

.edit-avatar-btn {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 32px;
  height: 32px;
  background: #b3f90f;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  transition: 0.2s;
}

.edit-avatar-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* SECTIONS */
.section-title {
  font-size: 20px;
  font-weight: 600;
  margin: 24px 0 12px;
  color: #1f1f1f;
}

/* FIELDS */
.field-group {
  margin-bottom: 16px;
}

.label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.input,
.select,
.textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 15px;
  background: #f9f9f9;
  transition: 0.2s;
  font-family: inherit;
}

.input:focus,
.select:focus,
.textarea:focus {
  outline: none;
  border-color: #b3f90f;
  background-color: #ffffff;
}

.textarea {
  min-height: 100px;
  resize: vertical;
  font-family: inherit;
}

.select {
  cursor: pointer;
}

/* CARD */
.card {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
  margin-bottom: 25px;
  border: 1px solid #e8e7ec;
}

/* GALLERY */
.gallery {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.gallery-item {
  aspect-ratio: 1;
  background: #e0e0e0;
  border-radius: 12px;
  position: relative;
  background-size: cover;
  background-position: center;
}

.geo-status {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
}

.geo-status.success {
  background-color: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}

.geo-status.warning {
  background-color: #fffbeb;
  color: #b45309;
  border: 1px solid #fcd34d;
}

.geo-icon {
  font-size: 16px;
}

.geo-link {
  color: #047857;
  text-decoration: underline;
  font-weight: 600;
  cursor: pointer;
}
.geo-link:hover {
  text-decoration: none;
}

.remove-gallery-btn {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 24px;
  height: 24px;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}

.gallery-item:hover .remove-gallery-btn {
  opacity: 1;
}

.gallery-upload {
  aspect-ratio: 1;
  border: 2px dashed #aab8ff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: #f5f7ff;
  transition: 0.25s ease;
}

.gallery-upload:hover {
  border-color: #2d3eff;
  background: #eef1ff;
}

.edit-icon {
  width: 20px;
  height: 20px;
}

.gallery-icon {
  width: 40px;
  height: 40px;
  margin-bottom: 8px;
}

.upload-text {
  font-size: 15px;
  color: #2d3eff;
  font-weight: 600;
  text-align: center;
}

/* POSITION */
.position-card {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff;
  padding: 12px 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.position-icon {
  font-size: 18px;
}

.position-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
}

.remove-icon {
  background: none;
  border: none;
  font-size: 18px;
  color: #999;
  cursor: pointer;
}

/* PLANS */
.plan-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.add-circle-btn {
  width: 32px;
  height: 32px;
  background: #b3f90f;
  border: none;
  border-radius: 12px;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
}

.add-circle-btn:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.plan-card {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 12px;
  border: 1px solid #e8e7ec;
}

.plan-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr auto;
  gap: 12px;
  align-items: end;
}

.plan-field {
  display: flex;
  flex-direction: column;
}

.remove-btn {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 8px;
}

/* CHECKBOXES */
.checkbox-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 14px;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #2196f3;
}

/* HOURS */
.hours-card {
  display: grid;
  grid-template-columns: 1.5fr 1fr 1fr;
  gap: 12px;
  align-items: center;
  background: #fff;
  padding: 16px 20px;
  border-radius: 8px;
  margin-bottom: 8px;
  border: 1px solid #e8e7ec;
}

.day-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.day-checkbox input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #2196f3;
}

.day-name {
  font-size: 14px;
}

.time-input {
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 14px;
}
</style>
