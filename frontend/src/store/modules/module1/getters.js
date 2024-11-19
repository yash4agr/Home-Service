const isLoggedIn = state => state.isLoggedIn
const isAuthenticated = state => true
const isEmailVerified = state => true
const currentUser = state => state.user
const loginDialogVisible = state => state.showLoginDialog
const signupDialogVisible = state => state.signupDialogVisible
const otpDialogVisible = state => state.otpDialogVisible
const resetPassDialogVisible = state => state.resetPassDialogVisible
const professionalSignupDialogVisible = state => state.professionalSignupDialogVisible
const isResetPasswordVerified = (state) => (email) => {
    return state.resetPasswordVerifiedEmails[email] === true;
  };
export default {
    isLoggedIn,
    isAuthenticated,
    isEmailVerified,
    currentUser,
    loginDialogVisible,
    signupDialogVisible,
    otpDialogVisible,
    resetPassDialogVisible,
    isResetPasswordVerified,
    professionalSignupDialogVisible,
    }