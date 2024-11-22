<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterView, RouterLink} from 'vue-router';
import axios from '@/plugins/axios';
import Navbar from './components/Navbar/Navbar.vue';

import Footer from './components/Footer.vue';


function handleSearch(searchTerm) {
  // Implement search logic
  console.log('Searching for:', searchTerm);
}
</script>


<template>
    <div class="app">
    <Navbar />
    </div>
    <div class="main-content">
      <router-view />
    </div>
    <Footer />
</template>

<style>
.app {
  /* min-height: 0vh; */
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
}

</style>


