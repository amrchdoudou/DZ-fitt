// api.js
import axios from 'axios';

// Configuration de l'API - détection automatique de l'URL
// Si vous utilisez une IP différente (comme 192.168.56.1), cette fonction l'utilisera automatiquement
const getApiBaseURL = () => {
  // Si une URL est définie dans les variables d'environnement, l'utiliser
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }

  // Sinon, détecter automatiquement selon l'URL du frontend
  const hostname = window.location.hostname;
  const port = '8000';

  // Si le frontend tourne sur localhost ou 127.0.0.1, utiliser localhost pour l'API
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return `http://localhost:${port}/api`;
  }

  // Sinon, utiliser la même IP que le frontend
  return `http://${hostname}:${port}/api`;
};

const API_BASE_URL = getApiBaseURL();
console.log('🔧 API Base URL:', API_BASE_URL);

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  const skipAuth = ['/login', '/register', '/verify-email', '/resend-verification-code'];
  if (token && !skipAuth.some(url => config.url.includes(url))) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default {
  // ========== AUTHENTICATION ==========
  register(data, isFormData = false) {
    const config = isFormData ? {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    } : {};
    return apiClient.post('/register/', data, config);
  },

  login(credentials) {
    return apiClient.post('/login/', credentials);
  },

  verifyEmail(data) {
    return apiClient.post('/verify-email/', data);
  },

  resendVerificationCode(data) {
    return apiClient.post('/resend-verification-code/', data);
  },

  forgotPassword(data) {
    return apiClient.post('/forgot-password/', data);
  },

  verifyResetCode(data) {
    return apiClient.post('/verify-reset-code/', data);
  },

  resetPassword(data) {
    return apiClient.post('/reset-password/', data);
  },

  setAuthToken(token) {
    if (token) {
      apiClient.defaults.headers.common['Authorization'] = `Token ${token}`;
      localStorage.setItem('authToken', token);
    } else {
      delete apiClient.defaults.headers.common['Authorization'];
      localStorage.removeItem('authToken');
    }
  },

  googleLogin(data) {
    return apiClient.post('/accounts/google/login/', data);
  },

  // ========== GÉRANT (SETTINGS) ==========
  updateFullName(data) {
    return apiClient.put('/gerant/update-full-name/', data);
  },

  changePassword(data) {
    return apiClient.put('/gerant/change-password/', data);
  },

  // ========== SALLES (PROFILE/MY GYM) ==========
  // Liste des salles du gérant
  getMySalles() {
    return apiClient.get('/my-salles/');
  },

  // Détails d'une salle
  getSalleDetail(salleId) {
    return apiClient.get(`/Detail-my-salle/${salleId}/`);
  },

  // Mettre à jour une salle
  updateSalle(salleId, data) {
    return apiClient.put(`/Detail-my-salle/${salleId}/`, data);
  },

  // Supprimer une salle
  deleteSalle(salleId) {
    return apiClient.delete(`/Detail-my-salle/${salleId}/`);
  },

  // Créer une nouvelle salle
  createSalle(data) {
    return apiClient.post('/my-salles/', data);
  },

  // ========== PHOTOS ==========
  // Liste des photos d'une salle
  getSallePhotos(salleId) {
    return apiClient.get(`/salles/${salleId}/photos/`);
  },

  // Ajouter une photo
  addSallePhoto(salleId, formData) {
    return apiClient.post(`/salles/${salleId}/photos/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Supprimer une photo
  deleteSallePhoto(salleId, photoId) {
    return apiClient.delete(`/salles/${salleId}/photos/${photoId}/`);
  },

  // ========== FORMULES D'ABONNEMENT ==========
  // Liste des formules d'une salle
  getFormules(salleId) {
    return apiClient.get(`/salles/${salleId}/formules/`);
  },

  // Créer une formule
  createFormule(salleId, data) {
    return apiClient.post(`/salles/${salleId}/formules/`, data);
  },

  // Mettre à jour une formule
  updateFormule(salleId, formuleId, data) {
    return apiClient.put(`/salles/${salleId}/formules/${formuleId}/`, data);
  },

  // Supprimer une formule
  deleteFormule(salleId, formuleId) {
    return apiClient.delete(`/salles/${salleId}/formules/${formuleId}/`);
  },

  // ========== ÉQUIPEMENTS ==========
  // Liste de tous les équipements disponibles
  getAllEquipements() {
    return apiClient.get('/equipment/');
  },

  // Liste des équipements d'une salle
  getSalleEquipements(salleId) {
    return apiClient.get(`/salles/${salleId}/equipe/`);
  },

  // Ajouter un équipement à une salle
  addSalleEquipement(salleId, data) {
    return apiClient.post(`/salles/${salleId}/equipe/add/`, data);
  },

  // Supprimer un équipement d'une salle
  deleteSalleEquipement(salleId, equipementId) {
    return apiClient.delete(`/salles/${salleId}/equipe/${equipementId}/delete/`);
  },

  // ========== SERVICES ==========
  // Liste de tous les services disponibles
  getAllServices() {
    return apiClient.get('/services/');
  },

  // Liste des services d'une salle
  getSalleServices(salleId) {
    return apiClient.get(`/salles/${salleId}/services/`);
  },

  // Ajouter un service à une salle
  addSalleService(salleId, serviceId) {
    return apiClient.post(`/salles/${salleId}/services/add/`, { service_id: serviceId });
  },

  // Supprimer un service d'une salle
  deleteSalleService(salleId, serviceId) {
    return apiClient.delete(`/salles/${salleId}/services/${serviceId}/`);
  },

  // ========== HORAIRES D'OUVERTURE (Gym Opening Hours) ==========
  // Liste des horaires d'une salle
  getSalleHoraires(salleId) {
    return apiClient.get(`/salles/${salleId}/horaires/`);
  },

  // Mettre à jour les horaires (Bulk)
  updateSalleHoraires(salleId, data) {
    return apiClient.put(`/salles/${salleId}/horaires/`, data);
  },

  // ========== EMPLOI DU TEMPS / COURS (Class Schedules) ==========
  // Liste des créneaux de cours d'une salle
  getSalleSchedules(salleId) {
    return apiClient.get(`/salles/${salleId}/schedules/`);
  },

  // Créer un créneau
  createSchedule(salleId, data) {
    return apiClient.post(`/salles/${salleId}/schedules/`, data);
  },

  // Mettre à jour un créneau
  updateSchedule(salleId, scheduleId, data) {
    return apiClient.put(`/salles/${salleId}/schedules/${scheduleId}/`, data);
  },

  // Supprimer un créneau
  deleteSchedule(salleId, scheduleId) {
    return apiClient.delete(`/salles/${salleId}/schedules/${scheduleId}/`);
  },

  // ========== COURSES ==========
  // Liste des cours d'une salle
  getCourses(salleId) {
    return apiClient.get(`/salles/${salleId}/courses/`);
  },

  // Créer un cours
  createCourse(salleId, data) {
    return apiClient.post(`/salles/${salleId}/courses/`, data);
  },

  // Mettre à jour un cours
  updateCourse(salleId, courseId, data) {
    return apiClient.put(`/salles/${salleId}/courses/${courseId}/`, data);
  },

  // Supprimer un cours
  deleteCourse(salleId, courseId) {
    return apiClient.delete(`/salles/${salleId}/courses/${courseId}/`);
  },

  // ========== AVIS/REVIEWS ==========
  // Get reviews for a specific salle
  getSalleAvis(salleId) {
    return apiClient.get(`/salles/${salleId}/avis/`);
  },

  // Create a review
  addAvis(salleId, data) {
    return apiClient.post(`/salles/${salleId}/avis/`, data);
  },

  // ========== GÉOCODAGE ==========
  geocodeAddress(address) {
    return apiClient.post('/geocode/', { address });
  },

  // ========== ITINÉRAIRE ==========
  getDirections(salleId, mode = 'driving', originLat = null, originLng = null) {
    const params = { mode };
    if (originLat) params.origin_lat = originLat;
    if (originLng) params.origin_lng = originLng;
    return apiClient.get(`/salles/${salleId}/directions/`, { params });
  },

  // ========== RECHERCHE DE SALLES ==========
  getFilters() {
    return apiClient.get('/filters/');
  },

  searchGyms(params) {
    // params can include: search, distance, equipment, services, hours, rating, lat, lng
    return apiClient.get('/salles/search/', { params });
  },

  // Get all public gyms (for search page)
  getAllGyms(params) {
    return apiClient.get('/salles/', { params });
  },

  // Get public gym details
  getPublicGym(id) {
    return apiClient.get(`/salles/${id}/`);
  },
};


