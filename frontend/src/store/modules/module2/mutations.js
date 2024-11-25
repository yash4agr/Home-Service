// Services
const SET_SERVICES_LIST = (state, services) => {
  state.services.list = services
  state.services.popular = services.filter(service => service.rating > 4)
  }
    
const SET_SERVICES_CATEGORIES = (state, categories) => {
  state.services.categories = categories
  }
    
const SET_SERVICES_LOADING = (state, isLoading) => {
  state.services.isLoading = isLoading
  }
    
const SET_SERVICES_ERROR = (state, error) => {
  state.services.error = error
  }

// Cart
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
  SET_SERVICES_LIST,
  SET_SERVICES_CATEGORIES,
  SET_SERVICES_LOADING,
  SET_SERVICES_ERROR,

  ADD_TO_CART,
  REMOVE_FROM_CART,
  TOGGLE_CART,
  SET_CART_OPEN,
    }