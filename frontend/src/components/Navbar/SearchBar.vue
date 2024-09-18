<script setup>
import TopBar from './TopBar.vue';
const emit = defineEmits(['search']);

function handleSearch(event) {
  emit('search', event.target.value);
}
</script>

<template>
  <div class="search-bar">
    <TopBar />
    <input 
      type="text" 
      placeholder="Search..." 
      @input="handleSearch"
    >
  </div>
</template>

<style scoped>
.search-bar {
  position: fixed;
  top: 0; 
  left: 0;
  right: 0;
  padding: 0.5rem 1rem;
  background-color: var(--body-color);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 100;
}

.search-bar input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

/* Add more styles as needed */
</style>