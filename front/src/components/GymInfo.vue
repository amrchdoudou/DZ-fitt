<template>
  <div class="gym-container">
    <!-- ABOUT GYM -->
    <div class="section">
      <h2 class="section-title">About Gym</h2>
      <p class="section-text">{{ gymData.about }}</p>
    </div>

    <!-- CONTACT US -->
    <div class="section">
      <h2 class="section-title">Contact Us</h2>
      <div class="contact-item">
        <span class="contact-icon">📱</span>
        <p class="contact-text">{{ gymData.phone }}</p>
      </div>
    </div>

    <!-- SERVICES -->
    <div class="section">
      <h2 class="section-title">Services</h2>
      <div class="tags-container">
        <span class="tag" v-for="service in gymData.services" :key="service">
          {{ service }}
        </span>
      </div>
    </div>

    <!-- EQUIPMENTS -->
    <div class="section">
      <h2 class="section-title">Equipments</h2>
      <div class="tags-container">
        <span class="tag" v-for="equipment in gymData.equipments" :key="equipment">
          {{ equipment }}
        </span>
      </div>
    </div>

    <!-- WORKING HOURS -->
    <div class="section">
      <h2 class="section-title">Working hours</h2>
      <table class="hours-table">
        <tr v-for="day in gymData.workingHours" :key="day.day">
          <td class="day-name">{{ day.day }}</td>
          <td class="hours-label" v-if="day.status !== 'Closed'">From</td>
          <td class="hours-time">{{ day.from }}</td>
          <td class="hours-label" v-if="day.status !== 'Closed'">To</td>
          <td class="hours-time" v-if="day.status !== 'Closed'">{{ day.to }}</td>
          <td class="closed" v-if="day.status === 'Closed'">{{ day.status }}</td>
        </tr>
      </table>
    </div>

  </div>
</template>

<script>
export default {
  name: 'GymInfo',
  props: {
    gym: {
      type: Object,
      required: true
    }
  },
  mounted() {
    // Debug: log the gym object to see its structure
    console.log('GymInfo - Full gym object:', this.gym);
    console.log('GymInfo - Services:', this.gym.services);
    console.log('GymInfo - Equipes:', this.gym.equipes);
    console.log('GymInfo - Horaires:', this.gym.horaires);
  },
  computed: {
    gymData() {
      // Use data directly from the gym prop
      const services = this.gym.services || [];
      const equipes = this.gym.equipes || [];
      const horaires = this.gym.horaires || [];
      
      console.log('Processing services:', services);
      console.log('Processing equipes:', equipes);
      console.log('Processing horaires:', horaires);
      
      return {
        about: this.gym.description || 'No description available',
        phone: this.gym.telephone || this.gym.phone || 'Not provided',
        // Extract service names - handle both string and object formats
        services: services.map(s => {
          if (typeof s === 'string') return s;
          return s.service_nom || s.nom || JSON.stringify(s);
        }),
        // Extract equipment names - handle both string and object formats
        equipments: equipes.map(e => {
          if (typeof e === 'string') return e;
          return e.equipement_nom || e.nom || JSON.stringify(e);
        }),
        // Working hours
        workingHours: horaires.map(h => ({
            day: h.jour || h.day || 'Unknown',
            from: h.heure_ouverture || h.from || '',
            to: h.heure_fermeture || h.to || '',
            status: h.est_ferme ? 'Closed' : 'Open'
        }))
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0px;
  padding: 0;
  box-sizing: border-box;
}

.gym-container {
  background-color: red;
  padding: 24px 32px 24px 32px;
  width: 100%;
  
  /* Removed margin: 0 auto to align content to the left */
  
  font-family: Arial, sans-serif;

  border-radius: 8px;
border: 1px solid var(--border-dash, #E8E7EC);
background: var(--surface-page, #FFF);
}

.section {
  background-color: white;
  padding: 0px;
  margin-bottom: 32px;
  border-radius: 0px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 15px;
  color: #000;
}

.section-text {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contact-icon {
  font-size: 16px;
}

.contact-text {
  font-size: 14px;
  color: #666;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: #e8f0ff;
  color: #2563eb;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.hours-table {
  width: 100%;
  border-collapse: collapse;
}

.hours-table tr {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}

.day-name {
 
  font-weight: 500;
  color: #000;
}

.hours-label {
  color: #999;
  
}

.hours-time {
  font-weight: bold;
  color: #000;
  
}

.closed {
  color: #999;
  font-weight: 500;
}


@media (max-width: 600px) {
  .gym-container {
    padding: 15px;
  }
  
  .section {
    padding: 15px;
    margin-bottom: 10px;
  }
}
</style>
