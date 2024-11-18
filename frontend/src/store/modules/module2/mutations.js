
const ADD_TO_CART = (state, service) => {
      const existingItem = state.cart.find(item => item.id === service.id)
      if (existingItem) {
        existingItem.quantity = 1
      } else {
        state.cart.push({
          ...service,
          quantity: 1
        })
      }
    }
    
const REMOVE_FROM_CART = (state, serviceId) => {
      const index = state.cart.findIndex(item => item.id === serviceId)
      if (index !== -1) {
        state.cart.splice(index, 1)
      }
    }
    
const TOGGLE_CART = (state) => {
      state.isCartOpen = !state.isCartOpen
    }
    
const SET_CART_OPEN = (state, isOpen) => {
      state.isCartOpen = isOpen
    }

export default {
    ADD_TO_CART,
    REMOVE_FROM_CART,
    TOGGLE_CART,
    SET_CART_OPEN,
    }