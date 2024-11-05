<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  cartItems: {
    type: Array,
    required: true
  },
  isCartOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['update:isCartOpen', 'removeFromCart'])

const cartTotal = computed(() => {
  return props.cartItems.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const toggleCart = () => {
  emit('update:isCartOpen', !props.isCartOpen)
}

const removeItem = (serviceId) => {
  emit('removeFromCart', serviceId)
}
</script>

<template>
  <div class="cart-container">
    <!-- Cart Icon with Badge -->
    <button class="cart-toggle icon" @click="toggleCart">
      <i class="ri-shopping-cart-line"></i>
      <span v-if="cartItems.length" class="cart-badge">{{ cartItems.length > 9? "9+" : cartItems.length }}</span>
    </button>

    <!-- Cart Sidebar -->
     
    <div class="cart-sidebar" :class="{ 'cart-open': isCartOpen }">
      <div class="cart-header">
        <h3>Your Cart</h3>
        <button class="close-cart" @click="toggleCart">×</button>
      </div>

      <div class="cart-items">
        <div v-if="cartItems.length === 0" class="empty-cart">
          Your cart is empty
        </div>
        <div v-else v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image" :alt="item.name">
          <div class="cart-item-details">
            <h4>{{ item.name }}</h4>
            <p>${{ item.price }}</p>
          </div>
          <button class="remove-item" @click="removeItem(item.id)">×</button>
        </div>
      </div>

      <div class="cart-footer" v-if="cartItems.length > 0">
        <div class="cart-total">
          <span>Total:</span>
          <span>${{ cartTotal.toFixed(2) }}</span>
        </div>
        <button class="checkout-btn">Proceed to Checkout</button>
      </div>
    </div>
  </div>
</template>

<style scoped>

.icon {
    background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  position: relative;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-container {
  position: relative;
}

.cart-toggle {
  position: relative;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  font-size: 1.25rem;
}

.cart-badge {
  position: absolute;
  top: -0.25px;
  right: -0.25px;
  background: #e11d48;
  color: white;
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.75rem;
  min-width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.cart-sidebar {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: #ffffff;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.cart-open {
  right: 0;
}

.cart-header {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-cart {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #1f2937;
}

.cart-items {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  position: relative;
}

.cart-item img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.cart-item-details {
  flex: 1;
}

.cart-item-details h4 {
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.cart-item-details p {
  margin: 0;
  color: #2563eb;
  font-weight: 600;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.quantity-controls button {
  background: #f3f4f6;
  border: none;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  border-radius: 4px;
}

.remove-item {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  color: #666;
}

.cart-footer {
  padding: 1rem;
  border-top: 1px solid #f3f4f6;
}

.cart-total {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-weight: 600;
}

.checkout-btn {
  width: 100%;
  padding: 1rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.checkout-btn:hover {
  background: #1e40af;
}

.empty-cart {
  text-align: center;
  padding: 2rem;
  color: #666;
}

/* Responsive Design */
@media (max-width: 768px) {
  .cart-sidebar {
    width: 100%;
    right: -100%;
  }
}

@media (max-width: 480px) {
  .cart-item {
    flex-direction: column;
  }
  
  .cart-item img {
    width: 100%;
    height: 160px;
  }
  
  .remove-item {
    top: 1rem;
    right: 1rem;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    padding: 0.25rem;
  }
}
</style>