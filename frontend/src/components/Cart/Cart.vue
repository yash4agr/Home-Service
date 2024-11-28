<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { RouterLink, useRouter } from 'vue-router'
import Booking from'@/components/Cart/BookNow.vue'

const store = useStore()
const router = useRouter()
const route = useRouter()

const props = defineProps({
  isCartOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:isCartOpen'])

// Get cart items from store
const cartItems = computed(() => store.getters['module2/cartItems'])
// Calculate total
const cartTotal = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.base_price * getServiceHours(item.id)), 0);
})

const toggleCart = () => {
  if (!props.isCartOpen) {
        router.push({ 
      query: { 
        ...route.query, 
        cart: 'true' 
      }
    });
  } else {
    // const query = { ...route.query };
    // delete query.cart;
    // router.push({
    //   path: route.path,
    //   query,
    //   hash: route.hash,
    // });
  }
  emit('update:isCartOpen', !props.isCartOpen)
}

const removeItem = (serviceId) => {
  store.dispatch('module2/removeFromCart', serviceId)
}

// Add service hours selection
const selectedHours = ref({})

const updateHours = (serviceId, hours) => {
  if (hours >= 1) {
    selectedHours.value[serviceId] = hours
    // You might want to update the store with the hours
    store.dispatch('module2/updateServiceHours', { serviceId, hours })
  }
}

// Get hours for a service
const getServiceHours = (serviceId) => {
  return selectedHours.value[serviceId] || 1 // Default to 1 hour
}

// Calculate service total
const getServiceTotal = (service) => {
  const hours = getServiceHours(service.id)
  return (service.base_price * hours).toFixed(2)
}

// Handle booking
const handleBooking = () => {
  router.push({ 
    query: { 
      ...route.query, 
      booking: 'true' 
    }
  });
  toggleCart()
}
</script>

<template>
  <div class="cart-container">
    <!-- Cart Icon with Badge -->
    <button class="cart-toggle nav-icon" @click="toggleCart">
      <i class="ri-shopping-cart-line"></i>
      <span v-if="cartItems.length" class="cart-badge">
        {{ cartItems.length > 9 ? "9+" : cartItems.length }}
      </span>
    </button>

    <!-- Cart Dialog -->
    <Transition name="fade">
      <div v-if="isCartOpen" class="cart-overlay" @click.self="toggleCart">
        <div class="cart-dialog">
          <div class="cart-header">
            <h2 class="cart-title">Your Cart</h2>
            <button class="cart-close" @click="toggleCart">
              <i class="ri-close-line" />
            </button>
          </div>

          <div class="cart-content">
            <div v-if="cartItems.length === 0" class="cart-empty">
              <i class="ri-shopping-cart-line cart-empty-icon"></i>
              <p>Your cart is empty</p>
            </div>
            
            <div v-else class="cart-items">
              <div v-for="item in cartItems" :key="item.id" class="cart-item">
                <img :src="item.img" :alt="item.name" class="cart-item-image">
                
                <div class="cart-item-details">
                  <h3 class="cart-item-title">{{ item.name }}</h3>
                  <p class="cart-item-price">₹{{ item.base_price }}/hr</p>
                  
                  <div class="hours-selector">
                    <label :for="'hours-' + item.id">Hours needed:</label>
                    <select 
                      :id="'hours-' + item.id"
                      :value="getServiceHours(item.id)"
                      @change="e => updateHours(item.id, parseInt(e.target.value))"
                      class="hours-select"
                    >
                      <option v-for="n in 8" :key="n" :value="n">{{ n }} {{ n === 1 ? 'hour' : 'hours' }}</option>
                    </select>
                  </div>

                  <p class="service-total">
                    Total: ₹{{ getServiceTotal(item) }}
                  </p>
                </div>

                <button 
                  class="remove-btn"
                  @click="removeItem(item.id)"
                  aria-label="Remove service"
                >
                  <i class="ri-delete-bin-line"></i>
                </button>
              </div>
            </div>
          </div>

          <div v-if="cartItems.length > 0" class="cart-footer">
            <div class="cart-total">
              <span>Total Amount</span>
              <span class="total-amount">₹{{ cartTotal.toFixed(2) }}</span>
            </div>
            <button class="book-btn" @click="handleBooking">Book Now</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
  <Booking />
</template>

<style scoped>
.cart-container {
  position: relative;
}

.cart-toggle {
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
  font-size: 1.25rem;
}


.cart-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: var(--accent-color);
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.75rem;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background-color: var(--background-color-blur);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  padding: 2rem 1.5rem;
}

.cart-dialog {
  position: relative;
  width: 100%;
  max-width: 500px;
  background: var(--container-color);
  border-radius: 1rem;
  box-shadow: 0 8px 32px var(--background-color-blur);
  animation: slideUp 0.3s ease-out;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 4rem);
}

.cart-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cart-title {
  font-size: var(--h2-font-size);
  color: var(--text-color);
  margin: 0;
}

.cart-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  color: var(--text-color);
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s;
}

.cart-close:hover {
  color: var(--primary-color);
}

.cart-content {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.cart-empty {
  text-align: center;
  padding: 2rem;
  color: var(--text-color-light);
}

.cart-empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--surface-color);
  border-radius: 0.5rem;
  position: relative;
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.cart-item-details {
  flex: 1;
}

.cart-item-title {
  margin: 0 0 0.5rem;
  font-size: 1rem;
  color: var(--text-color);
}

.cart-item-price {
  color: var(--primary-color);
  font-weight: 600;
}

.hours-selector {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.hours-select {
  background: var(--surface-hover);
  border: 1px solid var(--border-color);
  border-radius: 0.25rem;
  padding: 0.25rem 0.5rem;
  color: var(--text-color);
  font-size: 0.875rem;
}

.service-total {
  font-weight: 600;
  color: var(--primary-color);
  text-align: end;
}

.remove-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: transparent;
  border: none;
  color: var(--text-color-light);
  cursor: pointer;
  padding: 0.5rem;
  transition: color 0.2s;
}

.remove-btn:hover {
  color: var(--error-color);
}

.cart-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.cart-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-weight: 600;
  color: var(--text-color);
}

.total-amount {
  color: var(--primary-color);
  font-size: 1.25rem;
}

.book-btn {
  width: 100%;
  background-color: var(--accent-color);
  color: #fff;
  font-weight: var(--font-semi-bold);
  padding: 1rem;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color var(--transition-speed),
    transform var(--transition-speed), box-shadow var(--transition-speed);
}

.book-btn:hover {
  background-color: var(--secondary-color);
  transform: translateY(-1px);
  box-shadow: 0 4px 24px var(--secondary-color-blur);
}

.book-btn:active {
  transform: translateY(0);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .cart-overlay {
    padding: 1rem;
  }
  
  .cart-dialog {
    max-height: calc(100vh - 2rem);
  }
  
  .cart-item {
    flex-direction: column;
  }
  
  .cart-item-image {
    width: 100%;
    height: 160px;
  }
  
  .remove-btn {
    top: 0.5rem;
    right: 0.5rem;
  }
}
</style>