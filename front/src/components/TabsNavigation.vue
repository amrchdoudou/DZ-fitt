<template>
  <div class="tabs-navigation">
    <button 
      v-for="tab in tabs" 
      :key="tab"
      :class="['tab', { 'active': activeTab === tab }]"
      @click="$emit('update:activeTab', tab)"
    >
      {{ tab }}
    </button>
  </div>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  }
});

const tabs = ['Galerie', 'Reviews', 'Schedule', 'Courses'];

defineEmits(['update:activeTab']);
</script>

<style scoped>
.tabs-navigation {
width: 837px;

  display: flex;
  gap: 12px;
  padding: 0px 0px;
 
  background: white;
  height: 42px;
  align-items: center;
}

.tab {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  cursor: pointer;
  padding: 12px 8px;
  border-bottom: 3px solid transparent;
  height: 100%;
  display: flex;
  align-items: center;
  transition: all 0.2s;
}

.tab.active {
  color: #053ecd;
  border-bottom-color: #053ecd;
}

.tab:hover {
  color: #053ecd;
}
</style>
