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

const fetchBookings = async ({ commit }) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)

  try {
      const response = await axios.get('/api/bookings/get_bookings')
      console.log("bookings: ", response.data)
      commit('SET_BOOKINGS', response.data)
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.message || 'Failed to fetch bookings')
    } finally {
      commit('SET_LOADING', false)
    }
}

const cancelBooking = async ({ commit }, bookingId) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
      
  try {
    await axios.post('/api/professionals/service_actions', { "service_request_id" : bookingId, "action" : "canceled"})
    commit('REMOVE_BOOKING', bookingId)
  } catch (error) {
    commit('SET_ERROR', error.response?.data?.message || 'Failed to cancel booking')
  } finally {
    commit('SET_LOADING', false)
  }
}

const closeBooking = async ({ commit }, bookingId) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
      
  try {
    await axios.post('/api/professionals/service_actions', { "service_request_id" : bookingId, "action" : "completed"})
    commit('UPDATE_BOOKING', response.data)
  } catch (error) {
    commit('SET_ERROR', error.response?.data?.message || 'Failed to close booking')
  } finally {
    commit('SET_LOADING', false)
  }
}

const submitReview = async ({ commit }, { bookingId, rating, comment }) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
      
  try {
    const response = await axios.post('/api/bookings/submit_review', {
      "service_request_id": bookingId,
      "rating": rating,
      "review": comment
    })
    
    // Update the booking with review details
    commit('UPDATE_BOOKING', {
      id: bookingId,
      rating,
      review: comment
    })
  } catch (error) {
    commit('SET_ERROR', error.response?.data?.message || 'Failed to submit review')
  } finally {
    commit('SET_LOADING', false)
  }
}

const acceptService = async ({ commit }, serviceId) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
      
  try {
    await axios.post('/api/professionals/service_actions', { "service_request_id" : serviceId, "action" : "accept"})
    // Update the booking status
    commit('UPDATE_BOOKING', {
      id: serviceId,
      status: 'Accepted'
    })
  } catch (error) {
    commit('SET_ERROR', error.response?.data?.message || 'Failed to accept service')
  } finally {
    commit('SET_LOADING', false)
  }
}

const rejectService = async ({ commit }, serviceId) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
      
  try {
    await axios.post('/api/professionals/service_actions', { "service_request_id" : serviceId, "action" : "reject"})
    
    // Update the booking status
    commit('UPDATE_BOOKING', {
      id: serviceId,
      status: 'Rejected'
    })
  } catch (error) {
    commit('SET_ERROR', error.response?.data?.message || 'Failed to reject service')
  } finally {
    commit('SET_LOADING', false)
  }
}


const checkServiceability = async ({ commit }, { pincode, serviceIds }) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
  
  try {
    const response = await axios.get('/api/bookings/check-serviceability', {
      params: {
        pincode: pincode,
        serviceIds: serviceIds.join(',')
      }
    });
    
    commit('SET_LOADING', false)
    return response.data.serviceable
  } catch (error) {
    const errorMessage = error.response?.data?.message || 'Serviceability check failed'
    commit('SET_ERROR', errorMessage)
    commit('SET_LOADING', false)
    return false
  }
}

const createBooking = async ({ commit, rootState, rootGetters }, bookingData) => {
  commit('SET_LOADING', true)
  commit('SET_ERROR', null)
  try {
    const cartItems = rootGetters['module2/cartItems']
    
    // Validate booking data
    if (!cartItems || cartItems.length === 0) {
      throw new Error('No services selected for booking')
    }
    
    const formData = new FormData()
    
    // Personal Information
    formData.append('full_name', bookingData.fullName)
    formData.append('phone_number', bookingData.phoneNumber)
    
    // Address Details
    formData.append('locality', bookingData.address.locality)
    formData.append('city', bookingData.address.city)
    formData.append('state', bookingData.address.state)
    formData.append('pincode', bookingData.address.pincode)
    
    // Service Details
    formData.append('service_date', bookingData.serviceDate)
    formData.append('service_time', bookingData.serviceTime)
    formData.append('payment_method', bookingData.paymentMethod || 'cash')
    
    // Cart Items and Calculations
    const totalAmount = cartItems.reduce((total, item) => {
      const hours = rootState.module2.serviceHours[item.id] || 1
      return total + (item.base_price * hours)
    }, 0)
    formData.append('total_amount', String(totalAmount))
    

    // Add services as multiple form fields
    cartItems.forEach((item, index) => {
      const hours = rootState.module2.serviceHours[item.id] || 1
      formData.append(`services[${index}][service_id]`, String(item.id))
      formData.append(`services[${index}][hours]`, String(hours))
      formData.append(`services[${index}][base_price]`, String(item.base_price))
    })
    
    // Make API call to Flask backend
    const response = await axios.post('/api/bookings/create_booking', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    // Clear cart after successful booking
    commit('CLEAR_CART')
    commit('SET_LOADING', false)
    
    return response.data
  } catch (error) {
    const errorMessage = error.response?.data?.message || 'Booking creation failed'
    commit('SET_ERROR', errorMessage)
    commit('SET_LOADING', false)
    throw new Error(errorMessage)
  }
}


const addToCart = ({ commit }, service) => {
      commit('ADD_TO_CART', service)
    }
    
const removeFromCart = ({ commit }, serviceId) => {
      commit('REMOVE_FROM_CART', serviceId)
    }

const updateServiceHours = ({ commit }, payload) => {
    commit('UPDATE_SERVICE_HOURS', payload)
  }
    
const toggleCart = ({ commit }) => {
      commit('TOGGLE_CART')
    }
    
const setCartOpen = ({ commit }, isOpen) => {
      commit('SET_CART_OPEN', isOpen)
    }

const toggleBooking = ({ commit }) => {
  commit('TOGGLE_BOOKING')
}
    
const setBookingOpen = ({ commit }, isOpen) => {
  commit('SET_BOOKING_OPEN', isOpen)
}

const toggleBookingDialog = ({ commit }, isOpen) => {
  commit('TOGGLE_BOOKING_DIALOG', isOpen)
}



export default {
  fetchServices,
  fetchCategories,
    addToCart,
    removeFromCart,
    toggleCart,
    setCartOpen,

  checkServiceability,
  createBooking,
  updateServiceHours,
  toggleBookingDialog,

  toggleBooking,
  setBookingOpen,

  fetchBookings,
  cancelBooking,
  closeBooking,
  submitReview,
  acceptService,
  rejectService,
}