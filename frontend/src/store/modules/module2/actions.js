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
    addToCart,
    removeFromCart,
    toggleCart,
    setCartOpen,
    }