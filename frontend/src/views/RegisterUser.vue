<script setup>
import SocialLogin from '../components/SocialLogin.vue';



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

const handleRegistration = () => {
  
}

</script>

<template>
    <div class="register" id="register">
      <form action="" class="register__form">
        <h2>Sign up</h2>

        <div class="register__group">
            <div class="register__item">
                <label for="email" class="register__label">Email</label>
                <input type="email" class="register__input" placeholder="Enter your email" id="email">
            </div>

            <div class="register__item">
                <label for="password" class="register__label">Password</label>
                <input v-model="newPassword" type="password" class="register__input" placeholder="Enter your password" id="password"> 
            </div>

            <div class="register__item">
                <label for="confirm_password" class="register__label">Confirm Password</label>
                <input v-model="confirmPassword" type="password" class="register__input" placeholder="Confirm password" id="confirm_password">
            </div>
        </div>

        <div class="register__register">
            <p class="register__signup">
                Don't have an account? <RouterLink to="/register">Sign up</RouterLink>
            </p>

            <a href="/forgot_password" class="register__forgot">
                Forgot password?
            </a>

            <button class="register__button" type="submit">Log In</button>
            
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
</style>