<script setup>
import SocialLogin from '../components/SocialLogin.vue';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const email = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');

const handleRegistration = async () => {
  errorMessage.value = '';

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match';
    return;
  }

  let form = document.getElementById("register__form");
  let formData = new FormData(form);
  formData.append("email", email.value);
  formData.append("password", newPassword.value);
  formData.append("confirm_password", confirmPassword.value);

  try {
    const response = await fetch("http://127.0.0.1:5000/api/auth/register", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed');
    }
    
    // console.log("Registration successful:", data);
    router.push('/');
  } catch (error) {
    console.error("Registration Error:", error.message);
    errorMessage.value = error.message || 'An error occurred while registering';
  }
};
</script>

<template>
    <div class="register" id="register">
      <form @submit.prevent="handleRegistration" class="register__form" id="register__form">
        <h2>Sign up</h2>

        <div class="register__group">
            <div class="register__item">
                <label for="email" class="register__label">Email</label>
                <input v-model="email" type="email" class="register__input" placeholder="Enter your email" id="email" required>
            </div>

            <div class="register__item">
                <label for="password" class="register__label">Password</label>
                <input v-model="newPassword" type="password" class="register__input" placeholder="Enter your password" id="password" minlength="8" required> 
            </div>

            <div class="register__item">
                <label for="confirm_password" class="register__label">Confirm Password</label>
                <input v-model="confirmPassword" type="password" class="register__input" placeholder="Confirm password" id="confirm_password" minlength="8" required>
            </div>
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <div class="register__register">
            <p class="register__signup">
                Don't have an account? <RouterLink to="/register">Sign up</RouterLink>
            </p>

            <a href="/forgot-password" class="register__forgot">
                Forgot password?
            </a>

            <button class="register__button" type="submit">Sign up</button>
            
        </div>
        <div class="separator">
              <div class="line"></div>
              <p>OR</p>
              <div class="line"></div>
          </div>
        <div>
          <SocialLogin />
        
        </div>
      </form>
      
      <router-link class="ri-close-line register__close" id="register-close" to="/"></router-link>

      
    </div>
    
</template>

<style scoped>

.register {
    position: fixed;
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

.register__close {
    position: absolute;
    top: 2rem;
    /* right: 2rem; */
    left: 50%;
    transform: translateX(-50%);
    font-size: 1.5rem;
    color: var(--title-color);
    cursor: pointer;
}

.register__form{
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

.register__title {
    font-size: var(--h2-font-size);
    color: var(--title-color);
}

.register__group{
    display: grid;
    row-gap: 1rem;
}

.register__label {
    display: block;
    text-align: initial;
    color: var(--title-color);
    font-weight: var(--font-medium);
    margin-bottom: 0.25rem;    
}
.register__input {
  width: 100%;
  background-color: var(--container-color);
  border: 2px solid var(--border-color);
  padding: 1rem;
  border-radius: 0.5rem;
  color: var(--text-color);
}
.register__input::-moz-placeholder {
  color: var(--text-color);
}
.register__input::placeholder {
  color: var(--text-color);
}
.register__signup {
  margin-bottom: 0.5rem;
}
.register__signup a {
  color: var(--first-color);
}
.register__forgot {
  display: inline-block;
  color: var(--first-color);
  margin-bottom: 1.25rem;
}
.register__button {
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
.register__button:hover {
  box-shadow: 0 4px 24px hsla(230, 75%, 40%, 0.4);
}

.separator {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-color);
}

.separator .line {
  height: 1px;
  width: 40%;
  background-color: var(--border-color);
}

.error-message {
  color: var(--error-color);
}

</style>