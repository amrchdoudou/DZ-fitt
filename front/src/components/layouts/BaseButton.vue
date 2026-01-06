<template>
  <button 
    :class="['base-button', `variant-${variant}`, `size-${size}`]"
    @click="$emit('click', $event)"
  >
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'outlined', 'secondary'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  }
})

defineEmits(['click'])
</script>

<style scoped>
.base-button {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

/* Sizes */
.size-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.size-md {
  padding: 12px 24px;
  font-size: 16px;
}

.size-lg {
  padding: 16px 32px;
  font-size: 18px;
}

/* Variants */
.variant-primary {
  background: #B3F90F;
  color: #000;
}

.variant-primary:hover {
  background: #a0e00d;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(179, 249, 15, 0.3);
}

.variant-outlined {
  background: transparent;
  color: #B3F90F;
  border: 2px solid #B3F90F;
}

.variant-outlined:hover {
  background: rgba(179, 249, 15, 0.1);
  transform: translateY(-2px);
}

.variant-secondary {
  background: #2563eb;
  color: white;
}

.variant-secondary:hover {
  background: #1d4ed8;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.base-button:active {
  transform: translateY(0);
}
</style>
