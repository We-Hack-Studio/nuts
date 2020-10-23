import axios from 'axios';
import storage from './utils';
import store from './store';

export const annonInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});
annonInstance.interceptors.request.use(function(config) {
    config.headers['Content-Type'] = 'application/json';
    config.headers['Accept'] = 'application/json';
    return config;
});

export const authInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});

authInstance.interceptors.request.use(function(config) {
    config.headers['Content-Type'] = 'application/json';
    config.headers['Accept'] = 'application/json';
    if (store.state.authToken) {
        config.headers['Authorization'] = 'Token ' + store.state.authToken;
    }
    return config;
});

authInstance.interceptors.response.use(
    response => {
        return response;
    },
    error => {
        if (error.response.status === 401) {
            storage.clear();

            if (window.location.pathname !== '/login') {
                window.location.href = '/#/login';
                return null;
            }
        }

        return Promise.reject(error);
    },
);
