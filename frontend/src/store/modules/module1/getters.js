// User related getters
const isAuthenticated = state => state.isAuthenticated
const currentUser = state => state.user
const userRole = state => state.userRole || 'user'
const isEmailVerified = state => state.isVerified || false

const loginDialogVisible = state => state.showLoginDialog
const signupDialogVisible = state => state.signupDialogVisible
const otpDialogVisible = state => state.otpDialogVisible
const resetPassDialogVisible = state => state.resetPassDialogVisible
const professionalSignupDialogVisible = state => state.professionalSignupDialogVisible
const isResetPasswordVerified = (state) => (email) => {
    return state.resetPasswordVerifiedEmails[email] === true;
  };

// Verification getters
const getOtpResendTimeout = state => state.otpResendTimeout
const emailVerificationStatus = state => state.emailVerificationStatus
const resetPasswordVerified = state => state.resetPasswordVerified
const resetPasswordEmail = state => state.resetPasswordEmail

export default {
  isAuthenticated,
  currentUser,
  userRole,
  isEmailVerified,
    
  loginDialogVisible,
  signupDialogVisible,
  otpDialogVisible,
  resetPassDialogVisible,
  isResetPasswordVerified,
  professionalSignupDialogVisible,

  getOtpResendTimeout,
  emailVerificationStatus,
  resetPasswordVerified,
  resetPasswordEmail,
    }