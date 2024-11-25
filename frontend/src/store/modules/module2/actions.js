import axios from 'axios';
const fetchServices = async ({ commit }) => {
  try {
    commit('SET_SERVICES_LOADING', true)
    const response = await axios.get('/api/services')
    const data = await response.data
    
    commit('SET_SERVICES_LIST', data)
    return data
  } catch (error) {
    commit('SET_SERVICES_ERROR', error.message)
    throw error
  } finally {
    commit('SET_SERVICES_LOADING', false)
  }
}
const fetchCategories = async ({ commit }) => {
  try {
    const response = await axios.get('/api/services/categories')
    const data = await response.data
    
    commit('SET_SERVICES_CATEGORIES', data)
    return data
  } catch (error) {
    console.error('Error fetching categories:', error.message)
    throw error
  }
}


const addToCart = ({ commit }, service) => {
      commit('ADD_TO_CART', service)
    }
    
const removeFromCart = ({ commit }, serviceId) => {
      commit('REMOVE_FROM_CART', serviceId)
    }
    
const toggleCart = ({ commit }) => {
      commit('TOGGLE_CART')
    }
    
const setCartOpen = ({ commit }, isOpen) => {
      commit('SET_CART_OPEN', isOpen)
    }

export default {
  fetchServices,
  fetchCategories,
    addToCart,
    removeFromCart,
    toggleCart,
    setCartOpen,
    }