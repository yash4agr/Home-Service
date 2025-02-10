import axios from "axios";
import store from "@/store";

axios.defaults.baseURL = 'http://127.0.0.1:5000';

// Request interceptor
axios.interceptors.request.use(
    config => {
        // Don't add access token for refresh requests
        if (!config.url.includes('/refresh')) {
            const token = store.state.module1.accessToken;
            if (token) {
                config.headers['Authorization'] = `Bearer ${token}`;
            }
        }
        return config;
    },
    error => Promise.reject(error)
);

// Response interceptor for token refresh
axios.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                if (store.state.module1.accessToken){
                    await store.dispatch('module1/refreshAccessToken');
                }
                // Update the original request with new token
                const newToken = store.state.module1.accessToken;
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                
                return axios(originalRequest);
            } catch (refreshError) {
                // If refresh fails, logout and redirect
                await store.dispatch('module1/logout');
                window.location.href = '?login=true';
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export default axios;