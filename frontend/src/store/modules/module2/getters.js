// Services
const servicesList = state => state.services.list;
const servicesPopular = state => state.services.popular;
const serviceCategories = state => state.services.categories;
const isServicesLoading = state => state.services.isLoading;

const cartItems = state => state.cart
const cartTotal = state => state.cart.reduce((total, item) => total + (item.price * item.quantity), 0)
const cartItemCount = state => state.cart.reduce((count, item) => count + item.quantity, 0)
const isCartOpen = state => state.isCartOpen

export default {
    servicesList,
    servicesPopular,
    serviceCategories,
    isServicesLoading,
    
    cartItems,
    cartTotal,
    cartItemCount,
    isCartOpen,
    }