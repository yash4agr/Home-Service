<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterView, RouterLink} from 'vue-router';

import Navbar from './components/Navbar/Navbar.vue';
import SearchBar from './components/Navbar/SearchBar.vue';
import BottomNavbar from './components/Navbar/BottomNavbar.vue';

import Footer from './components/Footer.vue';

function handleSearch(searchTerm) {
  // Implement search logic
  console.log('Searching for:', searchTerm);
}
</script>


<template>
    <div class="app">
    <!-- Navbar for large screens -->
    <Navbar class="large-screen-only" />

    <!-- TopBar and SearchBar for small screens -->
    <div class="small-screen-only">
      
      <SearchBar @search="handleSearch" /> 
    </div>

  <div class="main-content">
    <router-view />
  </div>

  <BottomNavbar class="small-screen-only" />
  <Footer />
</div>
</template>

<style>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 120px; /* Adjust this value based on your navbar height */
}

/* Small screen styles */
@media (max-width: 767px) {
  .large-screen-only {
    display: none !important ; 
  }

  .main-content {
    padding-top: 120px; /* Adjust based on TopBar + SearchBar height */
    padding-bottom: 60px; /* Adjust based on BottomNavbar height */
  }
}

/* Large screen styles */
@media (min-width: 768px) {
  .small-screen-only {
    display: none !important;
  }

  .main-content {
    padding-top: 80px; /* Adjust based on Navbar height */
  }
}
</style>


