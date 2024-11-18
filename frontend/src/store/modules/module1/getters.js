const isLoggedIn = state => state.isLoggedIn
const currentUser = state => state.user
const loginDialogVisible = state => state.showLoginDialog
const signupDialogVisible = state => state.showSignupDialog

export default {
    isLoggedIn,
    currentUser,
    loginDialogVisible,
    signupDialogVisible
    }