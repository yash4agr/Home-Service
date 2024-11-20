<script setup>
import BaseAuth from "@/components/Auth/BaseAuth.vue";
import ResetPassword from "@/components/Auth/ResetPassword.vue";
import { ref, computed, watch, onMounted, onUnmounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import axios from "axios";

// Composables
const router = useRouter();
const route = useRoute();
const store = useStore();

// References
const resetPasswordComponent = ref(null);

// State
const otpDigits = ref(["", "", "", "", "", ""]);
const errorMessage = ref("");
const successMessage = ref("");
const isResending = ref(false);
const timer = ref(30);
const timerInterval = ref(null);
const isLoading = ref(false);
const previousRoute = ref(null);

// Computed
const isOpen = computed(() => store.getters["module1/otpDialogVisible"]);
const canResend = computed(() => timer.value === 0);

const verificationType = computed(() => {
  if (route.query["verify-email"]) return "email-verification";
  if (route.query["reset-password"]) return "password-reset";
  return "signup";
});

const verificationEmail = computed(() => {
  return route.query.email || "";
});

// Methods
const startResendTimer = () => {
  timer.value = 30;
  timerInterval.value = setInterval(() => {
    if (timer.value > 0) {
      timer.value--;
    } else {
      clearInterval(timerInterval.value);
    }
  }, 1000);
};

const handleInput = (index, event) => {
  const value = event.target.value;

  if (!/^\d*$/.test(value)) {
    event.target.value = otpDigits.value[index];
    return;
  }

  otpDigits.value[index] = value.slice(-1);

  if (value && index < 5) {
    event.target.nextElementSibling?.focus();
  }

  if (otpDigits.value.every((digit) => digit !== "")) {
    handleVerify();
  }
};

const handleKeydown = (index, event) => {
  if (event.key === "Backspace" && !otpDigits.value[index]) {
    otpDigits.value[index - 1] = "";
    event.target.previousElementSibling?.focus();
  }
};

const handleVerificationSuccess = async (response) => {
  successMessage.value = "Verification successful!";
  switch (verificationType.value) {
    case "signup":
      await store.dispatch("module1/completeSignup", response.data);
      router.push("/");
      break;
    case "password-reset":
      // Update URL to indicate reset password verification
      await store.dispatch('module1/setResetPasswordVerified', {
        email: verificationEmail.value,
        verified: true
      });
      
      // Update URL with reset password parameters
      router.push({
        query: {
          ...route.query,
          newPassword: "true",
          email: verificationEmail.value,
          verified: "true"
        }
      });

      // Open reset password dialog
      resetPasswordComponent.value.openPasswordResetDialog(verificationEmail.value);
      closeDialog();
      break;
    case "email-verification":
      await store.dispatch("module1/updateEmailVerification", true);
      if (route.query.fromBooking) {
        router.push(route.query.redirectTo || "/service-booking");
      } else {
        router.push("/");
      }
      break;
  }
};

const handleVerify = async () => {
  if (isLoading.value) return;

  const otp = otpDigits.value.join("");
  errorMessage.value = "";
  successMessage.value = "";
  isLoading.value = true;

  try {
    // const response = await axios.post("/api/auth/verify-otp", {
    //   email: verificationEmail.value,
    //   otp,
    //   type: verificationType.value,
    // });
    const response = ref();
    
    await handleVerificationSuccess(response);
  } catch (error) {
    console.error("Verification Error:", error);
    errorMessage.value =
      error.response?.data?.message || "Invalid verification code";
    otpDigits.value = ["", "", "", "", "", ""];
    document.querySelector(".otp-input")?.focus();
  } finally {
    isLoading.value = false;
  }
};

const handleSubmit = () => {
  handleVerify();
};

const resendOTP = async () => {
  if (!canResend.value || isResending.value) return;

  isResending.value = true;
  errorMessage.value = "";

  try {
    await axios.post("/api/auth/resend-otp", {
      email: verificationEmail.value,
      type: verificationType.value,
    });

    successMessage.value = "New verification code sent!";
    startResendTimer();
  } catch (error) {
    errorMessage.value = "Failed to resend code. Please try again.";
  } finally {
    isResending.value = false;
  }
};

const closeDialog = () => {
  const query = { ...route.query };
  
  // Remove verification-related query parameters
  delete query["verify-email"];
  delete query["reset-password"];
  delete query["email"];

  router.push({
    path: route.path,
    query,
    hash: route.hash,
  });

  store.dispatch("module1/toggleOtpDialog", false);
};

// Watchers
watch(
  () => [
    route.query["verify-email"],
    route.query["reset-password"],
    route.query.email,
  ],
  ([newVerifyEmail, newResetPassword, newEmail]) => {
    if (
      (newVerifyEmail === "true" || newResetPassword === "true") &&
      newEmail &&
      !isOpen.value
    ) {
      store.dispatch("module1/toggleOtpDialog", true);
    } else if (!newVerifyEmail && !newResetPassword && isOpen.value) {
      store.dispatch("module1/toggleOtpDialog", false);
    }
  },
  { immediate: true }
);

// Lifecycle Hooks
onMounted(() => {
  const currentRoute = router.currentRoute.value;
  // Only store if not already on verification modal
  if (
    !currentRoute.query["verify-email"] &&
    !currentRoute.query["reset-password"]
  ) {
    previousRoute.value = {
      fullPath: currentRoute.fullPath,
      path: currentRoute.path,
      query: { ...currentRoute.query },
      hash: currentRoute.hash,
    };
  }

  startResendTimer();
});

onUnmounted(() => {
  clearInterval(timerInterval.value);
});
</script>

<template>
  <BaseAuth 
    :title="verificationType === 'password-reset' ? 'Reset Password Verification' : 'Verify Your Email'" 
    :is-open="isOpen" 
    :on-close="closeDialog" 
    :previous-route="previousRoute"
    @submit="handleSubmit"
  >
    <p class="verification-text">
      {{ verificationType === 'password-reset' 
        ? 'To reset your password, please enter the verification code we sent to:' 
        : 'To verify your email, please enter the verification code we sent to:' 
      }}<br />
      <strong>{{ verificationEmail }}</strong>
    </p>

    <div class="otp-container">
      <input 
        v-for="(digit, index) in otpDigits" 
        :key="index" 
        v-model="otpDigits[index]" 
        type="text" 
        class="otp-input"
        maxlength="1" 
        :autofocus="index === 0" 
        @input="handleInput(index, $event)"
        @keydown="handleKeydown(index, $event)" 
        :disabled="isLoading" 
      />
    </div>

    <div v-if="errorMessage" class="error-container">
      <p class="error-message" role="alert">
        {{ errorMessage }}
      </p>
    </div>

    <p v-if="successMessage" class="success-message" role="alert">
      {{ successMessage }}
    </p>

    <div class="resend-container">
      <button 
        type="button" 
        class="resend-button" 
        :disabled="!canResend || isLoading" 
        @click="resendOTP"
      >
        {{ 
          isResending
            ? "Sending..." 
            : canResend
              ? "Resend Code"
              : `Resend in ${timer}s`
        }}
      </button>
    </div>

    <button 
      class="auth-button" 
      type="submit" 
      :disabled="otpDigits.some((digit) => !digit) || isLoading"
    >
      {{ isLoading ? "Verifying..." : "Verify" }}
    </button>
  </BaseAuth>
  
  <ResetPassword ref="resetPasswordComponent" />
</template>

<style scoped>
.verification-text {
  text-align: center;
  color: var(--text-color);
  margin-bottom: 1.5rem;
}

.otp-container {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.otp-input {
  width: 3rem;
  height: 3rem;
  text-align: center;
  font-size: 1.25rem;
  font-weight: var(--font-semi-bold);
  border: 2px solid var(--accent-color);
  border-radius: 0.5rem;
  background-color: var(--container-color);
  color: var(--text-color);
  transition: all var(--transition-speed);
}

.otp-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px var(--accent-color);
  outline: none;
}

.resend-container {
  text-align: center;
  margin-bottom: 1rem;
}

.resend-button {
  background: none;
  border: none;
  color: var(--primary-color);
  cursor: pointer;
  font-weight: var(--font-medium);
  transition: color var(--transition-speed);
}

.resend-button:disabled {
  color: var(--text-color-light);
  cursor: not-allowed;
}

.resend-button:not(:disabled):hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

.success-message {
  color: var(--success-color);
  background-color: var(--success-color-light);
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

@media (max-width: 468px) {
  .otp-container {
    gap: 0.25rem;
  }

  .otp-input {
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1rem;
  }
}
</style>
