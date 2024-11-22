<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import SocialLogin from "@/components/SocialLogin.vue";
import EmailVerification from "@/components/Auth/EmailVerification.vue";
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// State
const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const errorMessage = ref("");
const previousRoute = ref(null);
const isSubmitting = ref(false);

// Computed
const isOpen = computed(() => store.getters["module1/signupDialogVisible"]);

// Methods
const handleSignup = async () => {
  if (isSubmitting.value) return;
  errorMessage.value = "";

  if (password.value !== confirmPassword.value) {
    errorMessage.value = "Passwords do not match";
    return;
  }

  try {
    isSubmitting.value = true;
    await store.dispatch("module1/signup", {
      name: name.value,
      email: email.value,
      password: password.value,
      confirmPassword: confirmPassword.value
    });

    // Successful signup
    closeDialog();
    router.push({
      query: {
        "verify-email": "true",
        email: email.value,
      },
    });
  } catch (error) {
    console.error("Signup Error:", error.response?.data?.message || error.message);
    errorMessage.value = error.response?.data?.message || "An error occurred during signup";
  } finally {
    isSubmitting.value = false;
  }
};

const handleSubmit = () => {
  handleSignup();
};

const closeDialog = () => {
  if (route.query.signup === "true") {
    // Remove signup query parameter while preserving others
    const query = { ...route.query };
    delete query.signup;
    router.push({
      path: route.path,
      query,
      hash: route.hash,
    });
  }
  store.dispatch("module1/toggleSignupDialog", false);
};

const handleLogin = () => {
  closeDialog();
  router.push({
    query: {
      login: true,
    },
  });
};

// Watch for route changes to handle dialog state
watch(
  () => route.query.signup,
  (newValue) => {
    // Only update store if the value actually changed
    if (newValue === "true" && !isOpen.value) {
      store.dispatch("module1/toggleSignupDialog", true);
    } else if (!newValue && isOpen.value) {
      store.dispatch("module1/toggleSignupDialog", false);
    }
  },
  { immediate: true }
);

// Store the previous route when mounting
onMounted(() => {
  const currentRoute = router.currentRoute.value;
  // Only store the previous route if we're not already on the signup modal
  if (!currentRoute.query.signup) {
    previousRoute.value = {
      fullPath: currentRoute.fullPath,
      path: currentRoute.path,
      query: { ...currentRoute.query },
      hash: currentRoute.hash,
    };
  }

  // Check URL on mount and open dialog if needed
  if (route.query.signup === "true" && !isOpen.value) {
    store.dispatch("module1/toggleSignupDialog", true);
  }
});
</script>

<template>
  <BaseAuth
    title="Sign In"
    :is-open="isOpen"
    :on-close="closeDialog"
    :previous-route="previousRoute"
    @submit="handleSubmit"
  >
    <div class="form-group">
      <div class="form-item">
        <label for="name" class="form-label">Full Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          class="form-input"
          placeholder="Enter your full name"
          required
        />
      </div>

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
          placeholder="Create a password"
          minlength="8"
          required
        />
      </div>
      <div class="form-item">
        <label for="confirm-password" class="form-label"
          >Confirm Password</label
        >
        <input
          id="confirm-password"
          v-model="confirmPassword"
          type="password"
          class="form-input"
          placeholder="Confirm your password"
          minlength="8"
          required
        />
      </div>
    </div>

    <p v-if="errorMessage" class="error-message" role="alert">
      {{ errorMessage }}
    </p>

    <div class="auth-actions">
      <p class="auth-alternate">
        Already have an account?
        <a @click="handleLogin" class="auth-link"> Log In </a>
      </p>

      <button 
    class="auth-button" 
    type="submit" 
    :disabled="isSubmitting"
  >
    {{ isSubmitting ? 'Creating Account...' : 'Create Account' }}
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

<style scoped>
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
</style>
