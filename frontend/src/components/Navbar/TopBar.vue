<script setup>
import { ref } from 'vue';
import lightIcon from '@/assets/icons/light.svg';
import darkIcon from '@/assets/icons/dark.svg';

const currentTheme = ref('light');

function toggleTheme() {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', currentTheme.value);
  localStorage.setItem('theme', currentTheme.value);
}
</script>

<template>
  <div class="top-bar">
    <div class="location">
      <i class="location-icon"></i>
      <span>Current Location</span>
    </div>
    <button @click="toggleTheme" class="theme-toggle">
        <img :src="currentTheme === 'light' ? darkIcon : lightIcon" alt="Theme toggle" class="theme-icon"/>
    </button>
  </div>
</template>

<style scoped>

.theme-toggle {
  background-color: transparent;
  border: none;
  cursor: pointer;
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: var(--body-color);
  z-index: 100000;
}

/* Add more styles as needed */
</style>