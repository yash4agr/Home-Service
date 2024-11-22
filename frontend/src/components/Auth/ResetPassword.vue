<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import { ref, computed, watch, onMounted } from "vue";
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
const isPasswordResetVisible = ref(false);
const errorMessage = ref("");
const isSubmitting = ref(false);

const isOpen = computed(() => store.getters["module1/resetPassDialogVisible"]);

// Methods
const handleResetPassword = async () => {
  if (isSubmitting.value) return;
  errorMessage.value = "";

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
    isSubmitting.value = true;
    await store.dispatch("module1/resetPassword", {
      email: email.value,
      password: newPassword.value,
      confirmPassword: confirmPassword.value
    });

    // Reset password success handling
    await store.dispatch('module1/setResetPasswordVerified', {
      email: email.value,
      verified: false
    });

    closePasswordResetDialog();
    router.push('?login=true');
    errorMessage.value = "Password reset successfully"
  } catch (error) {
    console.error('Reset Password Error:', error);
    errorMessage.value = error.response?.data?.message || 'An error occurred while resetting password';
  } finally {
    isSubmitting.value = false;
  }
};

const handleSubmit = () => {
  handleResetPassword();
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

      <button 
      class="auth-button" 
      type="submit" 
      :disabled="isSubmitting"
    >
      {{ isSubmitting ? 'Reseting Password...' : 'Reset Password' }}
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