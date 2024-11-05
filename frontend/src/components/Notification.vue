<script setup>
import SocialLogin from '../components/SocialLogin.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const store = useStore();

const email = ref('');
const password = ref('');
const errorMessage = ref('');


</script>

<template>
  <div class="auth-container">
    <div class="auth-overlay">
      <form @submit.prevent="handleLogin" class="auth-form">
        <router-link 
          class="auth-close" 
          to="/"
          aria-label="Close">
          <i class="ri-close-line"></i>
        </router-link>

        <h2 class="auth-title">Log In</h2>

        <div class="form-group">
          <div class="form-item">
            <label for="email" class="form-label">Email</label>
            <input 
              v-model="email" 
              type="email" 
              class="form-input" 
              placeholder="Enter your email" 
              id="email" 
              required
            >
          </div>

          <div class="form-item">
            <label for="password" class="form-label">Password</label>
            <input 
              v-model="password" 
              type="password" 
              class="form-input" 
              placeholder="Enter your password" 
              id="password" 
              minlength="8" 
              required
            >
          </div>
        </div>

        <p v-if="errorMessage" class="error-message" role="alert">{{ errorMessage }}</p>

        <div class="auth-actions">
          <p class="auth-alternate">
            Don't have an account? 
            <router-link to="/register" class="auth-link">Sign up</router-link>
          </p>

          <router-link to="/forgot-password" class="auth-link">
            Forgot password?
          </router-link>

          <button class="auth-button" type="submit">Log In</button>
        </div>

        <div class="separator">
          <div class="line"></div>
          <p>OR</p>
          <div class="line"></div>
        </div>

        <SocialLogin />
      </form>
    </div>
  </div>
</template>

<style>
/* Create a separate auth.css file for these reusable styles */

:root {
  /* Add any missing CSS variables */
  --auth-max-width: 400px;
  --auth-padding: 2rem;
  --auth-border-radius: 1rem;
  --transition-speed: 0.2s;
}

/* Container for both login and register pages */
.auth-container {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-modal);
  overflow-y: auto; /* Enable scrolling */
  -webkit-overflow-scrolling: touch; /* Smooth scroll on iOS */
}

.auth-overlay {
  min-height: 100%;
  padding: 2rem 1.5rem;
  background-color: var(--background-color-blur);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Reusable form styles */
.auth-form {
  position: relative;
  width: 100%;
  max-width: var(--auth-max-width);
  background-color: var(--container-color);
  padding: var(--auth-padding);
  border-radius: var(--auth-border-radius);
  box-shadow: 0 8px 32px var(--background-color-blur);
  animation: slideUp 0.3s ease-out;
}

.auth-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  color: var(--title-color);
  cursor: pointer;
  transition: color var(--transition-speed);
}

.auth-close:hover {
  color: var(--first-color);
}

.auth-title {
  font-size: var(--h2-font-size);
  color: var(--title-color);
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
  color: var(--title-color);
  font-weight: var(--font-medium);
  text-align: left;
}

.form-input {
  width: 100%;
  background-color: var(--container-color);
  border: 2px solid var(--border-color);
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--text-color);
  transition: border-color var(--transition-speed),
              box-shadow var(--transition-speed);
}

.form-input:focus {
  border-color: var(--first-color);
  box-shadow: 0 0 0 2px var(--first-color-light);
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
  color: var(--first-color);
  text-decoration: none;
  transition: color var(--transition-speed);
}

.auth-link:hover {
  color: var(--first-color-dark);
  text-decoration: underline;
}

.auth-button {
  width: 100%;
  background-color: var(--first-color);
  color: #fff;
  font-weight: var(--font-semi-bold);
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color var(--transition-speed),
              transform var(--transition-speed),
              box-shadow var(--transition-speed);
}

.auth-button:hover {
  background-color: var(--first-color-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 24px hsla(230, 75%, 40%, 0.4);
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
  background-color: var(--border-color);
}

.separator p {
  color: var(--text-color-light);
  font-size: 0.875rem;
}

.error-message {
  color: var(--error-color);
  background-color: var(--error-color-light);
  padding: 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  text-align: center;
}

.g-btn-wrapper {
  display: flex !important; 
  justify-content: center;
}

/* Animation */
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .auth-overlay {
    padding: 1rem;
  }
  
  .auth-form {
    padding: 1.5rem;
  }
}

</style>