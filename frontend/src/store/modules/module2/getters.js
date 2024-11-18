const cartItems = state => state.cart
const cartTotal = state => state.cart.reduce((total, item) => total + (item.price * item.quantity), 0)
const cartItemCount = state => state.cart.reduce((count, item) => count + item.quantity, 0)
const isCartOpen = state => state.isCartOpen

export default {
    cartItems,
    cartTotal,
    cartItemCount,
    isCartOpen,
    }