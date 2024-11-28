<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import SocialLogin from "@/components/Auth/SocialLogin.vue";
import EmailVerification from "@/components/Auth/EmailVerification.vue";
import { ref, computed, watch, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// State
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const previousRoute = ref(null);
const isSubmitting = ref(false);

// Computed
const isOpen = computed(() => store.getters["module1/loginDialogVisible"]);

// Methods
const handleLogin = async () => {
  if (isSubmitting.value) return;
  errorMessage.value = "";
  try {
    isSubmitting.value = true;
    await store.dispatch("module1/login", {
      email: email.value,
      password: password.value
    });

    closeDialog();
    
    // Navigate to the previous route or home
    router.push(previousRoute.value?.fullPath || "/");
    
  } catch (error) {
    console.error("Login Error:", error.response?.data?.message || error.message);
    errorMessage.value = error.response?.data?.message || "An error occurred while logging in";
  } finally {
    isSubmitting.value = false;
  }
};

const handleSubmit = () => {
  handleLogin();
};

const closeDialog = () => {
  if (route.query.login === "true") {
    // Remove login query parameter while preserving others
    const query = { ...route.query };
    delete query.login;
    router.push({
      path: route.path,
      query,
      hash: route.hash,
    });
  }
  store.dispatch("module1/toggleLoginDialog", false);
};

// Redundant
const openDialog = () => {
  // Add login query parameter while preserving existing query params
  router.push({
    path: route.path,
    query: { ...route.query, login: "true" },
    hash: route.hash,
  });
  store.dispatch("module1/toggleLoginDialog", true);
};

const handlePasswordReset = () => {
  if (!email.value) {
    errorMessage.value = "Please enter your email first";
    return;
  }

  // Close login dialog and open verification
  closeDialog();
  router.push({
    query: {
      "reset-password": "true",
      email: email.value,
    },
  });
};

const handleSignup = () => {
  closeDialog();
  router.push({
    query: {
      signup: true,
    },
  });
};

// Watch for route changes to handle dialog state
watch(
  () => route.query.login,
  (newValue) => {
    // Only update store if the value actually changed
    if (newValue === "true" && !isOpen.value) {
      store.dispatch("module1/toggleLoginDialog", true);
    } else if (!newValue && isOpen.value) {
      store.dispatch("module1/toggleLoginDialog", false);
    }
  },
  { immediate: true }
);

// Store the previous route when mounting
onMounted(() => {
  const currentRoute = router.currentRoute.value;
  // Only store the previous route if we're not already on the login modal
  if (!currentRoute.query.login) {
    previousRoute.value = {
      fullPath: currentRoute.fullPath,
      path: currentRoute.path,
      query: { ...currentRoute.query },
      hash: currentRoute.hash,
    };
  }

  // Check URL on mount and open dialog if needed
  if (route.query.login === "true" && !isOpen.value) {
    store.dispatch("module1/toggleLoginDialog", true);
  }
});
</script>

<template>
  <BaseAuth
    title="Log In"
    :is-open="isOpen"
    :on-close="closeDialog"
    :previous-route="previousRoute"
    @submit="handleSubmit"
  >
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
        />
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
        />
      </div>
    </div>

    <div v-if="errorMessage" class="error-container">
      <p class="error-message" role="alert">
        {{ errorMessage }}
      </p>
    </div>

    <div class="auth-actions">
      <p class="auth-alternate">
        Don't have an account?
        <a @click="handleSignup" class="auth-link"> Sign up </a>
      </p>

      <a @click="handlePasswordReset" class="auth-link"> Forgot password? </a>

      <button 
    class="auth-button" 
    type="submit" 
    :disabled="isSubmitting"
  >
    {{ isSubmitting ? 'Logging in...' : 'Log In' }}
  </button>
    </div>

    <div class="separator">
      <div class="line" />
      <p>OR</p>
      <div class="line" />
    </div>

    <SocialLogin />
  </BaseAuth>
  <EmailVerification />
</template>

<style>
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
  cursor: pointer;
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
    transform var(--transition-speed), box-shadow var(--transition-speed);
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
.error-container {
  min-height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
