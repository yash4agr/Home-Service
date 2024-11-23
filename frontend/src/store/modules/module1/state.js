export default {

  // User information
  user: JSON.parse(localStorage.getItem('user')) || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  userRole: JSON.parse(localStorage.getItem('user'))?.role || null,
  isVerified: JSON.parse(localStorage.getItem('user'))?.is_email_verified || false,
  accessToken: localStorage.getItem('access_token') || null,
  refreshToken: localStorage.getItem('refresh_token') || null,

  // Dialog visibility states
  showLoginDialog: false,
  signupDialogVisible: false,
  otpDialogVisible: false,
  resetPassDialogVisible: false, 
  professionalSignupDialogVisible: false,

  // Verification and reset password states
  emailVerificationStatus: false,
  resetPasswordVerified: false,
  resetPasswordEmail: null,

  }