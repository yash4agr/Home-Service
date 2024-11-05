<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import { useStore } from 'vuex'
import { RouterLink, useRouter } from 'vue-router'
import Cart from '@/components/Cart.vue'
import Notification from '@/components/Notification.vue'

const router = useRouter()
const store = useStore()
const loggedIn = ref(false)
const isScrolled = ref(false)
const currentTheme = ref('light')
const currentLocation = ref('Loading location...')
const showProfileDropdown = ref(false)
const showProfileDropdown1 = ref(false)
const isLocationLoading = ref(true)
const profileRef = ref(null)

// Cart-related computed properties
const cartItems = computed(() => store.getters.cartItems)
const isCartOpen = computed({
  get: () => store.getters.isCartOpen,
  set: (value) => store.dispatch('setCartOpen', value)
})

// Notifications
const notifications = computed(() => store.getters.notifications || [])
const unreadNotifications = computed(() => 
  notifications.value.filter(n => !n.read).length
)

// Cart methods
const updateQuantity = (serviceId, change) => {
  store.dispatch('updateQuantity', { serviceId, change })
}

const removeFromCart = (serviceId) => {
  store.dispatch('removeFromCart', serviceId)
}

function handleScroll() {
  isScrolled.value = window.scrollY > 0
}

// Close dropdown when clicking outside
function handleClickOutside(event) {
  if (profileRef.value && !profileRef.value.contains(event.target)) {
    showProfileDropdown.value = false
  }
}

async function getCurrentLocation() {
  isLocationLoading.value = true
  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject,{
        timeout: 5000,
        maximumAge: 0
      })
    })
    const { latitude, longitude } = position.coords
    const response = await axios.post('/get-location', {
      latitude,
      longitude
    })

    currentLocation.value = response.data.results[0].name || 'Location not found'
  } catch (error) {
    currentLocation.value = 'Delhi'
    console.error("Location error:", error)
  }
}

function logout() {
  store.dispatch('logout')
  showProfileDropdown.value = false
  // Redirect to login page
  router.push('/login')
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('click', handleClickOutside)
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    currentTheme.value = savedTheme
    document.documentElement.setAttribute('data-theme', savedTheme)
  }
  getCurrentLocation()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('click', handleClickOutside)
})

function toggleTheme() {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  localStorage.setItem('theme', currentTheme.value)
}
</script>

<template>
  <div class="navbar-wrapper" :class="{ 'navbar-scrolled': isScrolled }">
    <!-- Desktop Navbar -->
    <nav class="navbar desktop-nav" aria-label="Main navigation">
      <div class="navbar-container">
        <div class="navbar-left">
          <RouterLink to="/" class="navbar-logo">
            <img src="@/assets/vue.svg" alt="Logo" class="h-8 w-auto" />
          </RouterLink>
          <div class="location-picker" @click="getCurrentLocation">
            <i class="ri-map-pin-line" aria-hidden="true"></i>
            <span>{{ currentLocation }}</span>
          </div>
        </div>

        <div class="navbar-right">
          <!-- Theme Toggle -->
          <button 
            class="nav-icon"
            @click="toggleTheme"
            :aria-label="currentTheme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'"
            >
            <i :class="currentTheme === 'light' ? 'ri-moon-line' : 'ri-sun-line'" aria-hidden="true"></i>
          </button>

          <!-- Notifications -->
          <RouterLink to="/notification" class="nav-icon" aria-label="Notifications">
            <i class="ri-notification-4-line" aria-hidden="true"></i>
            <span v-if="unreadNotifications" class="notification-badge" role="status">
              {{ unreadNotifications }}
            </span>
          </RouterLink>
          

          <!-- Cart -->
          <div class="nav-icon-wrapper">
            <!-- <button class="nav-icon" @click="isCartOpen = !isCartOpen">
              <i class="ri-shopping-cart-line"></i>
              <span v-if="cartItems.length" class="cart-badge">
                {{ cartItems.length }}
              </span>
            </button> -->
            <Cart
              v-model:isCartOpen="isCartOpen"
              :cartItems="cartItems"
              @updateQuantity="updateQuantity"
              @removeFromCart="removeFromCart"
            />
          </div>

          <!-- Bookings -->
          <RouterLink to="/bookings" class="nav-icon" aria-label="Bookings">
            <i class="ri-calendar-line" aria-hidden="true"></i>
          </RouterLink>

          <!-- Profile -->
          <div v-if="!loggedIn">
          <RouterLink to="/login" class="nav-icon" aria-label="Bookings">
            <i class="ri-user-3-line" aria-hidden="true"></i>
          </RouterLink>
          </div>
          <div v-else class="profile-dropdown" ref="profileRef">
            <button 
              class="nav-icon"
              @click="showProfileDropdown1 = !showProfileDropdown1"
            >
              <i class="ri-user-3-line"></i>
            </button>
            <div 
              v-if="showProfileDropdown1"
              class="dropdown-menu"
            >
              <button @click="logout" class="dropdown-item">
                <i class="ri-logout-box-line"></i>
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Mobile Navbar -->
    <nav class="navbar mobile-nav" aria-label="Mobile navigation">
      <!-- Top Bar -->
      <div class="mobile-top-bar">
        <RouterLink to="/" class="navbar-logo">
          <img src="@/assets/vue.svg" alt="Logo" class="h-6 w-auto" />
        </RouterLink>
        <div class="location-picker" @click="getCurrentLocation" aria-hidden="true">
          <i class="ri-map-pin-line"></i>
          <span>{{ currentLocation }}</span>
        </div>
      </div>

      <!-- Bottom Bar -->
      
    </nav>
  </div>

  <nav class="mobile-nav" aria-label="Mobile bottom navigation">
    <div class="mobile-bottom-bar">
        <button class="nav-icon" @click="toggleTheme" :aria-label="currentTheme === 'light' ? 'Switch to dark mode' : 'Switch to light mode'">
          <i :class="currentTheme === 'light' ? 'ri-moon-line' : 'ri-sun-line'" aria-hidden="true"></i>
        </button>

        <RouterLink to="/notification" class="nav-icon" aria-label="Notifications">
            <i class="ri-notification-4-line" aria-hidden="true"></i>
            <span v-if="unreadNotifications" class="notification-badge" role="status">
              {{ unreadNotifications }}
            </span>
          </RouterLink>

        <div class="nav-icon-wrapper">
            <Cart
              v-model:isCartOpen="isCartOpen"
              :cartItems="cartItems"
              @updateQuantity="updateQuantity"
              @removeFromCart="removeFromCart"
            />
          </div>

        <RouterLink to="/bookings" class="nav-icon" aria-label="Bookings">
          <i class="ri-calendar-line" aria-hidden="true"></i>
        </RouterLink>

        <div v-if="!loggedIn">
          <RouterLink to="/login" class="nav-icon" aria-label="Bookings">
            <i class="ri-user-3-line" aria-hidden="true"></i>
          </RouterLink>
          </div>
          <div v-else class="profile-dropdown" ref="profileRef">
            <button 
              class="nav-icon"
              @click="showProfileDropdown = !showProfileDropdown"
              aria-expanded="showProfileDropdown"
              aria-label="Profile menu"
            >
              <i class="ri-user-3-line" aria-hidden="true"></i>
            </button>
            <div 
              v-if="showProfileDropdown"
              class="dropdown-menu dropdown-menu-mobile"
              role="menu"
            >
              <button @click="logout" class="dropdown-item" role="menuitem">
                <i class="ri-logout-box-line" aria-hidden="true"></i>
                Logout
              </button>
            </div>
          </div>
      </div>
    </nav>
</template>

<style scoped>
.navbar-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: var(--bg-color);
  transition: all 0.3s ease;
}

.navbar-scrolled {
  background-color: rgba(var(--surface-overlay-rgb), 0.7);
  backdrop-filter: blur(8px);
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.location-picker {
  display: flex;
  align-items: center;
  cursor: pointer;
  gap: 0.5rem;
  color: var(--primary-color);
  font-size: 0.875rem;
}

.nav-icon {
  background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  position: relative;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.nav-icon i {
  font-size: 1.25rem;
}

.notification-badge {
  position: absolute;
  top: -0.25rem;
  right: -0.25rem;
  background-color: var(--primary-color);
  color: white;
  border-radius: 9999px;
  padding: 0.125rem 0.375rem;
  font-size: 0.75rem;
  min-width: 1.25rem;
  text-align: center;
}

.profile-dropdown {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: var(--bg-color);
  border-radius: 0.375rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  min-width: 150px;
  margin-top: 0.5rem;
  z-index: 10001;
  transform-origin: top right;
  animation: dropdownFade 0.2s ease;
}

.dropdown-menu-mobile {
  bottom: 100%;
  top: auto;
  margin-top: 0;
  margin-bottom: 0.5rem;
  transform-origin: bottom right;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  width: 100%;
  text-align: left;
  border: none;
  background: transparent;
  color: var(--text-color);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: var(--surface-hover);
}

/* Mobile Styles */
.mobile-nav {
  display: none;
}

.mobile-top-bar {
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
}

.mobile-bottom-bar {
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: space-around;
  align-items: center;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--bg-color);
  border-top: 1px solid var(--border-color);
  z-index: 1000;
}


@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .mobile-nav {
    display: block;
  }

}
</style>