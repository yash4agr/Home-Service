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

const UPDATE_SERVICE_HOURS = (state, { serviceId, hours }) => {
  state.serviceHours[serviceId] = hours
  
  const cartItem = state.cartItems.find(item => item.id === serviceId)
  if (cartItem) {
    cartItem.hours = hours
  }
}

// Cart
const SET_CART_ITEMS = (state, items) => {
  state.cartItems = items
}

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


const TOGGLE_BOOKING = (state) => {
  state.isBookingOpen = !state.isBookingOpen
}
    
const SET_BOOKING_OPEN = (state, isOpen) => {
    state.isBookingOpen = isOpen
  }

const TOGGLE_BOOKING_DIALOG = (state, isOpen) => {
    state.bookingDialogOpen = isOpen
  }
const SET_ERROR = (state, error) => {
    state.error = error
  }
const SET_LOADING = (state, isLoading) => {
    state.loading = isLoading
  }
const CLEAR_CART = (state) => {
    state.cartItems = []
    state.serviceHours = {}
  }


const SET_BOOKINGS = (state, booking) => {
  state.bookings = booking
}
const ADD_BOOKING = (state, booking) => {
  state.bookings.push(booking)
}
const REMOVE_BOOKING = (state, bookingId) => {
  state.bookings = state.bookings.filter(booking => booking.id !== bookingId)
}

const UPDATE_BOOKING = (state, updatedBooking) => {
  const index = state.bookings.findIndex(booking => booking.id === updatedBooking.id)
  if (index !== -1) {
    state.bookings.splice(index, 1, updatedBooking)
  }
}



export default {
  SET_SERVICES_LIST,
  SET_SERVICES_CATEGORIES,
  SET_SERVICES_LOADING,
  SET_SERVICES_ERROR,
  UPDATE_SERVICE_HOURS,

  SET_CART_ITEMS,
  ADD_TO_CART,
  REMOVE_FROM_CART,
  TOGGLE_CART,
  SET_CART_OPEN,

  TOGGLE_BOOKING,
  SET_BOOKING_OPEN,

  TOGGLE_BOOKING_DIALOG, 
  SET_ERROR, 
  SET_LOADING, 
  CLEAR_CART, 

  SET_BOOKINGS,
  ADD_BOOKING,
  REMOVE_BOOKING,
  UPDATE_BOOKING
    }