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
const SET_RESET_PASSWORD_VERIFIED = (state, { email, verified }) => {
  state.resetPasswordVerifiedEmails = {
    ...state.resetPasswordVerifiedEmails,
    [email]: verified
  };
}
const SET_AUTH = (state, { user, token }) => {
    state.isLoggedIn = true;
    state.user = user;
    state.token = token;
  }
const CLEAR_AUTH = (state) => {
    state.isLoggedIn = false;
    state.user = null;
    state.token = null;
  }

export default {
    SET_LOGIN_DIALOG,
    SET_SIGNUP_DIALOG,
    SET_OTP_DIALOG,
    SET_RESET_PASSWORD_VERIFIED,
    SET_RESETPASS_DIALOG,
    SET_PROFESSIONAL_SIGNUP_DIALOG,
    SET_AUTH,
    CLEAR_AUTH,
}