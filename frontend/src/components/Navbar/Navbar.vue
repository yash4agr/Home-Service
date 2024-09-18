<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import lightIcon from '@/assets/icons/light.svg';
import darkIcon from '@/assets/icons/dark.svg';


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

        <button @click="toggleTheme" class="theme-toggle">
          <img :src="currentTheme === 'light' ? darkIcon : lightIcon" alt="Theme toggle" class="theme-icon"/>
        </button>

        <a href="#" class="navbar-link"><i class="fa-regular fa-bell icon"></i></a>
        <a href="#" class="navbar-link"><i class="fa-regular fa-cart-shopping icon"></i></a>
        <a href="#" class="navbar-link"><i class="fa-regular fa-clipboard-list icon"></i></a>
        <a href="#" class="navbar-link"><i class="fa-regular fa-user icon"></i></a>
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
}

.theme-toggle {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: var(--body-color);
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