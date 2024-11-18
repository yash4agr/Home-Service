<script setup>
import SocialLogin from '@/components/SocialLogin.vue';
import SignupDialog from '@/components/Auth/Signup.vue'
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
import axios from 'axios'

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// State
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const scrollPosition = ref(0);
const previousRoute = ref(null);

// Computed
const isOpen = computed(() => store.getters['module1/loginDialogVisible']);

// Methods
const handleLogin = async () => {
  errorMessage.value = '';
  const formData = new FormData();
  formData.append('email', email.value);
  formData.append('password', password.value);

  try {
    const response = await axios.post('/api/auth/login', formData , {
      headers: {
      'Content-Type': 'multipart/form-data'
      }
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }
    
    await store.dispatch('module1/loginSuccess', data);
    closeDialog();
    // Navigate to the previous route or home
    router.push(previousRoute.value?.fullPath || '/');
  } catch (error) {
    console.error('Login Error:', error.message);
    errorMessage.value = error.message || 'An error occurred while logging in';
  }
};

const closeDialog = () => {
  if (route.query.login === 'true') {
    // Remove login query parameter while preserving others
    const query = { ...route.query };
    delete query.login;
    router.push({ 
      path: route.path, 
      query,
      hash: route.hash 
    });
  }
  store.dispatch('module1/toggleLoginDialog', false);
};


// Redundant
const openDialog = () => {
  // Add login query parameter while preserving existing query params
  router.push({ 
    path: route.path,
    query: { ...route.query, login: 'true' },
    hash: route.hash
  });
  store.dispatch('module1/toggleLoginDialog', true);
};

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

// Watch for route changes to handle dialog state
watch(
  () => route.query.login,
  (newValue) => {
    // Only update store if the value actually changed
    if (newValue === 'true' && !isOpen.value) {
      store.dispatch('module1/toggleLoginDialog', true);
    } else if (!newValue && isOpen.value) {
      store.dispatch('module1/toggleLoginDialog', false);
    }
  },
  { immediate: true }
);

// Watch dialog state to handle body scroll
watch(isOpen, (newValue) => {
  if (newValue) {
    handleDialogOpen();
  } else {
    handleDialogClose();
  }
});

// Store the previous route when mounting
onMounted(() => {
  const currentRoute = router.currentRoute.value;
  // Only store the previous route if we're not already on the login modal
  if (!currentRoute.query.login) {
    previousRoute.value = {
      fullPath: currentRoute.fullPath,
      path: currentRoute.path,
      query: { ...currentRoute.query },
      hash: currentRoute.hash
    };
  }

  // Check URL on mount and open dialog if needed
  if (route.query.login === 'true' && !isOpen.value) {
    store.dispatch('module1/toggleLoginDialog', true);
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
      @click.self="closeDialog"
    >
      <div class="auth-overlay">
        <form @submit.prevent="handleLogin" class="auth-form">
          <button 
            type="button"
            class="auth-close" 
            @click="closeDialog"
            aria-label="Close"
          >
            <i class="ri-close-line" />
          </button>

          <h2 class="auth-title">Log In</h2>

          <div class="form-group">
            <div class="form-item">
              <label for="email" class="form-label">Email</label>
              <input 
                id="email"
                v-model="email" 
                type="email" 
                class="form-input" 
                placeholder="Enter your email"
                required
              >
            </div>

            <div class="form-item">
              <label for="password" class="form-label">Password</label>
              <input 
                id="password"
                v-model="password" 
                type="password" 
                class="form-input" 
                placeholder="Enter your password"
                minlength="8" 
                required
              >
            </div>
          </div>

          <p 
            v-if="errorMessage" 
            class="error-message" 
            role="alert"
          >
            {{ errorMessage }}
          </p>

          <div class="auth-actions">
            <p class="auth-alternate">
              Don't have an account? 
              <router-link to="?signup=true" class="auth-link" @click="handleDialogOpen">
                Sign up
              <SignupDialog />
              </router-link>
            </p>

            <router-link to="/forgot-password" class="auth-link">
              Forgot password?
            </router-link>

            <button class="auth-button" type="submit">
              Log In
            </button>
          </div>

          <div class="separator">
            <div class="line" />
            <p>OR</p>
            <div class="line" />
          </div>

          <SocialLogin />
        </form>
      </div>
    </div>
  </Transition>
</template>

<style>
:root {
  --auth-max-width: 400px;
  --auth-padding: 2rem;
  --auth-border-radius: 1rem;
  --transition-speed: 0.2s;
}

.auth-container {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100vh;
  z-index: 1100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-overlay {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
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

.form-group {
  display: grid;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-item {
  display: grid;
  gap: 0.25rem;
}

.form-label {
  color: var(--text-color);
  font-weight: var(--font-medium);
}

.form-input {
  width: 100%;
  background-color: var(--container-color);
  border: 2px solid var(--accent-color);
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--text-color);
  transition: border-color var(--transition-speed),
              box-shadow var(--transition-speed);
}

.form-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--accent-color);
  outline: none;
}

.form-input::placeholder {
  color: var(--text-color-light);
}

.auth-actions {
  display: grid;
  gap: 1rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-alternate {
  color: var(--text-color);
}

.auth-link {
  color: var(--primary-color);
  text-decoration: none;
  transition: color var(--transition-speed);
}

.auth-link:hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

.auth-button {
  width: 100%;
  background-color: var(--accent-color);
  color: #fff;
  font-weight: var(--font-semi-bold);
  padding: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color var(--transition-speed),
              transform var(--transition-speed),
              box-shadow var(--transition-speed);
}

.auth-button:hover {
  background-color: var(--secondary-color);
  transform: translateY(-1px);
  box-shadow: 0 4px 24px var(--secondary-color-blur);
}

.auth-button:active {
  transform: translateY(0);
}

.separator {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
}

.separator .line {
  flex: 1;
  height: 1px;
  background-color: var(--accent-color);
}

.separator p {
  color: var(--text-color-light);
  font-size: 0.875rem;
}

.error-message {
  color: var(--text-color-light);
  background-color: var(--error-color-light);
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
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