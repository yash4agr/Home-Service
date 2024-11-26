import axios from 'axios';

// User relatef actions
const signup = async ({ commit }, userData) => {
  try {
    const formData = new FormData();
    Object.keys(userData).forEach(key => {
      formData.append(key, userData[key]);
    });

    const response = await axios.post('/api/auth/register', formData, {
      headers:{
        "Content-Type": "multipart/form-data"
      }
    });

    const {access_token, refresh_token, user} = response.data;
    commit('SET_TOKENS', {
      accessToken: access_token,
      refreshToken: refresh_token
    });

    commit('SET_USER', user);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const login = async ({ commit }, credentials) => {
  try {
    const formData = new FormData();
    Object.keys(credentials).forEach(key => {
      formData.append(key, credentials[key]);
    });

    const response = await axios.post('/api/auth/login', formData, {
      headers:{
        "Content-Type": "multipart/form-data"
      }
    });

    const { access_token, refresh_token, user } = response.data;
    
    commit('SET_TOKENS', {
      accessToken: access_token,
      refreshToken: refresh_token
    });

    commit('SET_USER', user);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const googleLogin = async ({ commit }, userData) => {
  try {
    const response = await axios.post('/api/auth/google-login', { userData });
    
    const { access_token, refresh_token, user } = response.data;
    
    commit('SET_TOKENS', {
      accessToken: access_token,
      refreshToken: refresh_token
    });

    commit('SET_USER', user);
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);

    return response.data;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const fetchUserProfile = async ({ commit, state }) => {
  try {
    // Set up axios to use the access token
    const config = {
      headers: { 
        Authorization: `Bearer ${state.accessToken}` 
      }
    };

    const response = await axios.get('/api/auth/profile', config);
    
    commit('SET_USER', response.data);
    return response.data;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const refreshAccessToken = async ({ commit, state }) => {
  try {
    const response = await axios.get('/api/auth/refresh', {
      headers: {
        'Authorization': `Bearer ${state.refreshToken}`
      }
    });
    
    commit('SET_TOKENS', { 
      accessToken: response.data.access_token,
      refreshToken: state.refreshToken 
    });

    return response.data.access_token;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const verifyOTP = async  ({ commit }, { email, otp, type }) => {
  try {
    const response = await axios.post('/api/auth/verify-otp', {
      email,
      otp,
      type
    });
    commit('UPDATE_EMAIL_VERIFICATION', true)
    return response.data;
  } catch (error) {
    throw error;
  }
}

const OTP_TIMEOUT_DURATION = 10000; 
const resendOTP = async  ({ commit, state }, { email, type }) => {
  try {
    if (state.otpResendTimeout) {
      throw new Error('Please wait before requesting another OTP');
    }
    const response = await axios.post('/api/auth/resend-otp', {
      email,
      type
    });

    // commit('SET_OTP_RESEND_TIMEOUT', true);
    
    // // Clear timeout after duration
    // setTimeout(() => {
    //   commit('SET_OTP_RESEND_TIMEOUT', false);
    // }, OTP_TIMEOUT_DURATION);

    return response.data;
  } catch (error) {
    throw error;
  }
}

const resetPassword = async ({ commit }, userData) => {
  try {
    const formData = new FormData();
    Object.keys(userData).forEach(key => {
      formData.append(key, userData[key]);
    });

    const response = await axios.post('/api/auth/reset-password', formData, {
      headers:{
        "Content-Type": "multipart/form-data"
      }
    });

    return response.data;
  } catch (error) {
    commit('CLEAR_AUTH');
    throw error;
  }
}

const registerProfessional = async ({ commit }, professionalData) => {
  try {
    const formData = new FormData();
    Object.entries(professionalData).forEach(([key, value]) => {
      // Handle nested objects like address
      if (typeof value === 'object' && value !== null) {
        if (value instanceof File) {
          formData.append(key, value);
        } else {
          Object.entries(value).forEach(([nestedKey, nestedValue]) => {
            formData.append(`${key}.${nestedKey}`, nestedValue);
          });
        }
      } else {
        formData.append(key, value);
      }
    });

    const response = await axios.post('/api/professionals/signup', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    commit('SET_USER', response.data);
    return response.data;
  } catch (error) {
    throw error;
  }
};
  
const logout = ({ commit }) => {
    commit('CLEAR_AUTH');
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('cart');
  }

export default {
  signup,
  login,
  googleLogin,
  fetchUserProfile,
  refreshAccessToken,
  verifyOTP,
  resendOTP,
  resetPassword,
  registerProfessional,
  logout,

  // Dialog toggles
  toggleLoginDialog: ({ commit }, value) => commit('SET_LOGIN_DIALOG', value),
  toggleSignupDialog: ({ commit }, value) => commit('SET_SIGNUP_DIALOG', value),
  toggleOtpDialog: ({ commit }, value) => commit('SET_OTP_DIALOG', value),
  toggleResetPassDialog: ({ commit }, value) => commit('SET_RESETPASS_DIALOG', value),
  toggleProfessionalSignupDialog: ({ commit }, value) => commit('SET_PROFESSIONAL_SIGNUP_DIALOG', value),

  // Verification actions
  updateEmailVerification: ({ commit }, value) => commit('UPDATE_EMAIL_VERIFICATION', value),
  setResetPasswordVerified: ({ commit }, { email, verified }) => 
    commit('SET_RESET_PASSWORD_VERIFIED', { email, verified })
};


