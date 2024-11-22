import axios from "axios";
import store from "@/store";

// Set base URL for all axios requests
axios.defaults.baseURL = 'http://localhost:5000';

// Request interceptor
axios.interceptors.request.use(
    config => {
        const token = store.state.module1.accessToken;
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// // Response interceptor for token refresh
// axios.interceptors.response.use(
//     response => response,
//     async error => {
//         const originalRequest = error.config;

//         if (error.response.status === 401 && !originalRequest._retry) {
//             originalRequest._retry = true;

//             try {
//                 await store.dispatch('auth/refreshAccessToken');
                
//                 return axios(originalRequest);
//             } catch (refreshError) {
//                 store.dispatch('auth/logout');
                
//                 window.location.href = '?login=true';
                
//                 return Promise.reject(refreshError);
//             }
//         }

//         return Promise.reject(error);
//     }
// );

export default axios;