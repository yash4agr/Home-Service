<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  // Dialog visibility state from Vuex
  isOpen: {
    type: Boolean,
    required: true
  },
  // Function to close dialog and clean up route query
  onClose: {
    type: Function,
    required: true
  },
  // Optional previous route to return to after successful auth
  previousRoute: {
    type: Object,
    default: null
  }
});

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// State
const scrollPosition = ref(0);

// Dialog scroll management
const handleDialogOpen = () => {
  scrollPosition.value = window.scrollY;
  document.body.classList.add('dialog-open');
  document.body.style.position = 'fixed';
  document.body.style.top = `-${scrollPosition.value}px`;
  document.body.style.width = '100%';
};

const handleDialogClose = () => {
  document.body.style.position = '';
  document.body.style.top = '';
  document.body.style.width = '';
  document.body.classList.remove('dialog-open');
  window.scrollTo(0, scrollPosition.value);
};

// Watch dialog state to handle body scroll
watch(() => props.isOpen, (newValue) => {
  if (newValue) {
    handleDialogOpen();
  } else {
    handleDialogClose();
  }
});

// Cleanup
onUnmounted(() => {
  handleDialogClose();
});
</script>

<template>
  <Transition name="fade">
    <div
      v-if="isOpen"
      class="auth-container"
      @click.self="onClose"
    >
      <div class="auth-overlay">
        <form @submit.prevent="$emit('submit')" class="auth-form">
          <button 
            type="button"
            class="auth-close" 
            @click="onClose"
            aria-label="Close"
          >
            <i class="ri-close-line" />
          </button>

          <h2 class="auth-title">{{ title }}</h2>

          <!-- Form content passed via slot -->
          <slot />
        </form>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
:root {
  --auth-max-width: 400px;
  --auth-padding: 2rem;
  --auth-border-radius: 1rem;
  --transition-speed: 0.2s;
}

.auth-container {
  position: fixed;
  z-index: 1100;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.auth-overlay {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--background-color-blur);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  z-index: 1100;
}

.auth-form {
  position: relative;
  width: 100%;
  max-width: var(--auth-max-width);
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px var(--background-color-blur);
  animation: slideUp 0.3s ease-out;
  margin: auto;
  max-height: calc(100vh - 4rem);
  overflow-y: auto;
}

.auth-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  color: var(--text-color);
  background-color: transparent;
  border: none;
  cursor: pointer;
  transition: color var(--transition-speed);
}

.auth-close:hover {
  color: var(--primary-color);
}

.auth-title {
  font-size: var(--h2-font-size);
  color: var(--text-color);
  text-align: center;
  margin-bottom: 1.5rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .auth-overlay {
    padding: 1rem;
  }
  
  .auth-form {
    padding: 1.5rem;
    margin: 1rem;
    max-height: calc(100vh - 2rem);
  }
}
</style>