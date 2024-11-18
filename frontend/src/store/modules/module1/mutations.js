const SET_LOGIN_DIALOG = (state, value) => {
    state.showLoginDialog = value;
  }
const SET_SIGNUP_DIALOG = (state, value) => {
    state.showSignupDialog = value;
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
    SET_AUTH,
    CLEAR_AUTH,
}