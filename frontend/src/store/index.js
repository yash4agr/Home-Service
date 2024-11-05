import { createStore } from 'vuex'

export default createStore({
  state: {
    cart: [],
    isCartOpen: false
  },
  
  mutations: {
    ADD_TO_CART(state, service) {
      const existingItem = state.cart.find(item => item.id === service.id)
      if (existingItem) {
        existingItem.quantity = 1
      } else {
        state.cart.push({
          ...service,
          quantity: 1
        })
      }
    },
    
    REMOVE_FROM_CART(state, serviceId) {
      const index = state.cart.findIndex(item => item.id === serviceId)
      if (index !== -1) {
        state.cart.splice(index, 1)
      }
    },
    
    
    TOGGLE_CART(state) {
      state.isCartOpen = !state.isCartOpen
    },
    
    SET_CART_OPEN(state, isOpen) {
      state.isCartOpen = isOpen
    }
  },
  
  actions: {
    addToCart({ commit }, service) {
      commit('ADD_TO_CART', service)
    },
    
    removeFromCart({ commit }, serviceId) {
      commit('REMOVE_FROM_CART', serviceId)
    },
    
    toggleCart({ commit }) {
      commit('TOGGLE_CART')
    },
    
    setCartOpen({ commit }, isOpen) {
      commit('SET_CART_OPEN', isOpen)
    }
  },
  
  getters: {
    cartItems: state => state.cart,
    cartTotal: state => state.cart.reduce((total, item) => total + (item.price * item.quantity), 0),
    cartItemCount: state => state.cart.reduce((count, item) => count + item.quantity, 0),
    isCartOpen: state => state.isCartOpen
  }
})