<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import { ref, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import axios from "axios";

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// State
const email = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const isPasswordResetVisible = ref(false);

// Computed
const isResetPasswordVerified = computed(() => 
  store.getters['module1/isResetPasswordVerified'](email.value)
);

// Methods
const handleResetPassword = async () => {
  // Reset password validation
  if (!email.value) {
    errorMessage.value = 'Email is required';
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return;
  }

  if (newPassword.value.length < 8) {
    errorMessage.value = 'Password must be at least 8 characters long';
    return;
  }

  try {
    const formData = new FormData();
    formData.append('email', email.value);
    formData.append('newPassword', newPassword.value);

    const response = await axios.post('/api/auth/reset-password', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    // Reset password success handling
    await store.dispatch('module1/setResetPasswordVerified', {
      email: email.value,
      verified: false
    });

    // Show success message or toast
    store.dispatch('module1/showNotification', {
      message: 'Password reset successfully',
      type: 'success'
    });

    // Close password reset dialog
    closePasswordResetDialog();

    // Redirect to login
    router.push({ name: 'login' });
  } catch (error) {
    console.error('Reset Password Error:', error);
    errorMessage.value = error.response?.data?.message || 'An error occurred while resetting password';
  }
};

const openPasswordResetDialog = (userEmail) => {
  email.value = userEmail;
  isPasswordResetVisible.value = true;
  errorMessage.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
};

const closePasswordResetDialog = () => {
  isPasswordResetVisible.value = false;
  email.value = '';
  newPassword.value = '';
  confirmPassword.value = '';
  errorMessage.value = '';
};

// Expose methods to parent component
defineExpose({
  openPasswordResetDialog
});
</script>

<template>
  <BaseAuth 
    v-if="isPasswordResetVisible"
    title="Reset Password" 
    :is-open="isPasswordResetVisible"
    :on-close="closePasswordResetDialog"
    @submit="handleResetPassword"
  >
    <div class="form-group">
      <div class="form-item">
        <label for="email" class="form-label">Email</label>
        <input 
          id="email"
          v-model="email" 
          type="email" 
          class="form-input form-input-disabled" 
          disabled
        >
      </div>

      <div class="form-item">
        <label for="newPassword" class="form-label">New Password</label>
        <input 
          id="newPassword"
          v-model="newPassword" 
          type="password" 
          class="form-input" 
          placeholder="Enter new password"
          minlength="8"
          required
        >
      </div>

      <div class="form-item">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input 
          id="confirmPassword"
          v-model="confirmPassword" 
          type="password" 
          class="form-input" 
          placeholder="Confirm new password"
          minlength="8"
          required
        >
      </div>
    </div>

    <div v-if="errorMessage" class="error-container">
      <p class="error-message" role="alert">
        {{ errorMessage }}
      </p>
    </div>

    <div class="auth-actions">
      <p class="auth-alternate">
        Remember your password? 
        <router-link to="/?login=true" class="auth-link">
          Log in
        </router-link>
      </p>

      <button class="auth-button" type="submit">
        Reset Password
      </button>
    </div>
  </BaseAuth>
</template>

<style scoped>
.form-input-disabled {
  background-color: var(--container-color-light);
  cursor: not-allowed;
  opacity: 0.7;
}
.error-container {
  min-height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>