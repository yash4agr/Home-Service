// User related mutations
const SET_USER = (state, user) => {
  state.user = user;
  state.userRole = user.role;
  state.isVerified = user.is_email_verified
  state.isAuthenticated = !!user;
}

const SET_TOKENS = (state, {accessToken, refreshToken}) => {
  state.accessToken = accessToken;
  state.refreshToken = refreshToken;
  state.isAuthenticated = !!accessToken;
}

const CLEAR_AUTH = (state) => {
  state.user = null;
  state.isAuthenticated = false;
  state.accessToken = null;
  state.refreshToken = null;
}

// Dialog visibility mutations
const SET_LOGIN_DIALOG = (state, value) => {
    state.showLoginDialog = value;
  }
const SET_SIGNUP_DIALOG = (state, value) => {
    state.signupDialogVisible = value;
  }
const SET_OTP_DIALOG = (state, value) => {
  state.otpDialogVisible = value;
}
const SET_RESETPASS_DIALOG = (state, value) => {
  state.resetPassDialogVisible = value;
}
const SET_PROFESSIONAL_SIGNUP_DIALOG = (state, value) => {
  state.professionalSignupDialogVisible = value;
}

// Verification and reset mutations
const UPDATE_EMAIL_VERIFICATION = (state, value) => {
  let userData = JSON.parse(localStorage.getItem('user'))
  userData.isVerified = true
  localStorage.setItem('user', JSON.stringify(userData))
  state.isEmailVerified = true;
  state.emailVerificationStatus = true;
}
const SET_RESET_PASSWORD_VERIFIED = (state, { email, verified }) => {
    state.resetPasswordVerified = verified;
    state.resetPasswordEmail = email;
}


export default {
  // User
  SET_USER,
  SET_TOKENS,
  CLEAR_AUTH,

  // Dialogs
  SET_LOGIN_DIALOG,
  SET_SIGNUP_DIALOG,
  SET_OTP_DIALOG,
  SET_RESETPASS_DIALOG,
  SET_PROFESSIONAL_SIGNUP_DIALOG,

  // Verification & Password reset
  UPDATE_EMAIL_VERIFICATION,
  SET_RESET_PASSWORD_VERIFIED,
}