const toggleLoginDialog = ({ commit }, value) => {
    commit('SET_LOGIN_DIALOG', value);
  }
const toggleSignupDialog = ({ commit }, value) => {
    commit('SET_SIGNUP_DIALOG', value);
}
const loginSuccess = async ({ commit }, data) => {
    commit('SET_AUTH', {
      user: data.user,
      token: data.token
    });
    localStorage.setItem('token', data.token); // Store token in localStorage
    commit('SET_LOGIN_DIALOG', false); // Close dialog after successful login
  }
  
const logout = ({ commit }) => {
    commit('CLEAR_AUTH');
    localStorage.removeItem('token');
  }

export default {
    toggleLoginDialog,
    toggleSignupDialog,
    loginSuccess,
    logout,
}


