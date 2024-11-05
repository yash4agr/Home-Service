<script setup>
import { ref } from 'vue';

const isLoggedIn = ref(false); // Replace with actual auth logic

function toggleLogin() {
  isLoggedIn.value = !isLoggedIn.value;
}
</script>

<template>
  <nav class="bottom-navbar">
    <a href="#" class="nav-item">
      <i class="home-icon"></i>
      <span>Home</span>
    </a>
    <a href="#" class="nav-item">
      <i class="notification-icon"></i>
        <span>Notification</span>
    </a>
    <a href="#" class="nav-item">
      <i class="cart-icon"></i>
      <span>Cart</span>
    </a>
    <a href="#" class="nav-item">
      <i class="booking-icon"></i>
      <span>Booking</span>
    </a>
    <div v-if="!isLoggedIn" class="nav-item" @click="toggleLogin">
      <i class="login-icon"></i>
      <span>Login</span>
    </div>
    <div v-else class="nav-item dropdown">
      <i class="profile-icon"></i>
      <span>Profile</span>
      <!-- Add dropdown menu items here -->
    </div>
  </nav>
</template>

<style scoped>
.bottom-navbar {
  padding: 0.5rem 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--body-color);
  box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: var(--text-color);
}

/* Add more styles as needed */
</style>