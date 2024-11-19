const toggleLoginDialog = ({ commit }, value) => {
    commit('SET_LOGIN_DIALOG', value);
  }
const toggleSignupDialog = ({ commit }, value) => {
    commit('SET_SIGNUP_DIALOG', value);
}
const toggleOtpDialog = ({ commit }, value) => {
  commit('SET_OTP_DIALOG', value);
}
const toggleResetPassDialog = ({ commit }, value) => {
  commit('SET_RESETPASS_DIALOG', value);
}
const toggleProfessionalSignupDialog = ({ commit }, value) => {
  commit('SET_PROFESSIONAL_SIGNUP_DIALOG', value);
}
const setResetPasswordVerified = ({ commit }, { email, verified }) => {
  commit('SET_RESET_PASSWORD_VERIFIED', { email, verified });
};
const loginSuccess = async ({ commit }, data) => {
    commit('SET_AUTH', {
      user: data.user,
      token: data.token
    });
    localStorage.setItem('token', data.token); // Store token in localStorage
    commit('SET_LOGIN_DIALOG', false); // Close dialog after successful login
  }

  const registerProfessional = async ({ commit }, data) => {
    commit('SET_Professional', {
      user: data.user,
      token: data.token
    });
    localStorage.setItem('token', data.token); // Store token in localStorage
    commit('SET_PROFESSIONAL_SIGNUP_DIALOG', false); // Close dialog after successful login
  }
  
const logout = ({ commit }) => {
    commit('CLEAR_AUTH');
    localStorage.removeItem('token');
  }

export default {
    toggleLoginDialog,
    toggleSignupDialog,
    toggleOtpDialog,
    toggleResetPassDialog,
    toggleProfessionalSignupDialog,
    setResetPasswordVerified,
    registerProfessional,
    loginSuccess,
    logout,
}


