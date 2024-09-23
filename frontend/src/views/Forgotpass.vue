<script setup>
import { ref } from 'vue';

const step = ref(1); // 1: Email, 2: OTP, 3: Reset Password
const email = ref('');
const otp = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const handleEmailSubmit = () => {
  // Send email to backend to initiate OTP process
  console.log('Email submitted:', email.value);
  // Simulate backend response
  setTimeout(() => {
    step.value = 2;
  }, 1000);
};

const handleOtpSubmit = () => {
  // Verify OTP with backend
  if (!/^[0-9]{6}$/.test(otp.value)) {
    alert('Invalid OTP');
    return;
  }
  console.log('OTP submitted:', otp.value);
  // Simulate backend response
  setTimeout(() => {
    step.value = 3;
  }, 1000);
};

const handlePasswordReset = () => {
  if (newPassword.value !== confirmPassword.value) {
    alert('Passwords do not match');
    return;
  }
  // Send new password to backend to reset
  console.log('Password reset:', newPassword.value);
  // Simulate backend response
  setTimeout(() => {
    alert('Password reset successful');
    step.value = 1; // Reset to initial step
  }, 1000);
};
</script>

<template>
  <div class="reset-password">
    <form v-if="step === 1" @submit.prevent="handleEmailSubmit" class="reset-password__form">
      <h2>Enter Your Email</h2>
      <div class="reset-password__group">
        <label for="email" class="reset-password__label">Email</label>
        <input v-model="email" type="email" class="reset-password__input" placeholder="Enter your email" id="email" required>
      </div>
      <button class="reset-password__button" type="submit">Send OTP</button>
    </form>

    <form v-if="step === 2" @submit.prevent="handleOtpSubmit" class="reset-password__form">
      <h2>Enter OTP</h2>
      <div class="reset-password__group">
        <label for="otp" class="reset-password__label">Enter 6 digit OTP sent to:</label>
           <p class="user_email">{{ email }}</p>
        <input v-model="otp" type="text" class="reset-password__input" placeholder="Enter the OTP" id="otp" required>
      </div>
      <button class="reset-password__button" type="submit">Verify</button>
    </form>

    <form v-if="step === 3" @submit.prevent="handlePasswordReset" class="reset-password__form">
      <h2>Reset Password</h2>
      <div class="reset-password__group">
        <label for="newPassword" class="reset-password__label">New Password</label>
        <input v-model="newPassword" type="password" class="reset-password__input" placeholder="Enter new password" id="newPassword" minlength="8" required>
      </div>
      <div class="reset-password__group">
        <label for="confirmPassword" class="reset-password__label">Confirm Password</label>
        <input v-model="confirmPassword" type="password" class="reset-password__input" placeholder="Confirm new password" id="confirmPassword" minlength="8" required>
      </div>
      <button class="reset-password__button" type="submit">Submit</button>
    </form>
    <router-link class="ri-close-line close" id="register-close" to="/"></router-link>
  </div>
  
</template>

<style scoped>
.reset-password {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  z-index: var(--z-modal);
  background-color: var(--background-color-blur);
  -webkit-backdrop-filter: blur(24px);
  backdrop-filter: blur(24px);
  padding: 8rem 1.5rem 0;
  opacity: 1;
  /* pointer-events: none; */
  transition: opacity 0.2s;
}

.reset-password__form {
  display: grid;
  background-color: var(--container-color);
  padding: 3rem 2rem 3.5rem;
  box-shadow: 0 8px 32px var(--background-color-blur);
  border-radius: 1rem;
  row-gap: 1.25rem;
  text-align: center;
  transform: translateY(-1rem);
  transition: transform 0.2s;
  max-width: 400px;
  margin-inline: auto;
}

.reset-password__label {
  display: block;
    text-align: initial;
    color: var(--title-color);
    font-weight: var(--font-medium);
    margin-bottom: 0.25rem;   
}

.reset-password__input {
  width: 100%;
  background-color: var(--container-color);
  border: 2px solid var(--border-color);
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--text-color);
}

.reset-password__button {
  display: inline-block;
  background-color: var(--first-color);
  width: 100%;
  color: #fff;
  font-weight: var(--font-semi-bold);
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: box-shadow 0.4s;
}

.reset-password__button:hover {
  box-shadow: 0 4px 24px hsla(230, 75%, 40%, 0.4);
}

.user_email{
  margin: 0.25rem;
}

.close {
    position: absolute;
    top: 2rem;
    /* right: 2rem; */
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.5rem;
    color: var(--title-color);
    cursor: pointer;
}
</style>