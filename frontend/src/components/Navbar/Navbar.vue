<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isScrolled = ref(false); 
const currentTheme = ref('light');


function handleScroll() {
  isScrolled.value = window.scrollY > 0;
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    currentTheme.value = savedTheme;
    document.documentElement.setAttribute('data-theme', savedTheme);
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});

function toggleTheme() {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme.value);
  localStorage.setItem('theme', currentTheme.value);

}
</script>

<template>
  <nav class="navbar" :class="{ 'navbar-scrolled': isScrolled }">
    <div class="navbar-container">
      <a href="/" class="navbar-logo">
        <!-- Your logo here --> logo
      </a>

      <div class="navbar-actions">
        <input type="text" placeholder="Search..." class="search-input">
        <span class="location">Current Location</span>
        
      </div>
      
      <div class="navbar-menu">

          <i :class="currentTheme === 'light' ? 'ri-moon-line' : 'ri-sun-line'" class="icon" @click="toggleTheme"></i>
          <!-- <img :src="currentTheme === 'light' ? darkIcon : lightIcon" alt="Theme toggle" class="theme-icon"/> -->

        <RouterLink to="/login" class="navbar-link"><i class="ri-notification-4-line icon"></i></RouterLink>
          <RouterLink to="/login" class="navbar-link"><i class="ri-shopping-cart-line icon"></i></RouterLink>
            <RouterLink to="/login" class="navbar-link"><i class="ri-survey-line icon"></i></RouterLink>
        <RouterLink to="/login" class="navbar-link"><i class="ri-user-3-line icon"></i></RouterLink>
      </div>

    </div>
  </nav>
</template>

<style scoped>

.icon {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  font-size: 1.5rem;
  transition: background-color .3s ease, color .3s ease;
  color: var(--title-color);
}

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: var(--body-color);
  transition: background-color .3s ease, color .3s ease;
  /* box-shadow: 0 2px 4px rgba(0,0,0,0.1); */
  z-index: 1000;
}

.navbar-scrolled {
  background-color: rgba(var(--surface-overlay-rgb), 0.7);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Add more styles as needed */
</style>