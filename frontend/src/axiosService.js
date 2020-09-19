import axios from 'axios';
import store from './store';
import storage from './utils';

export const annonInstance = axios.create({
  baseURL: window.conf.restApiBaseUrl,
  timeout: 10000,
});
annonInstance.interceptors.request.use(function(config) {
  config.headers['Content-Type'] = 'application/vnd.api+json';
  config.headers['Accept'] = 'application/vnd.api+json';
  return config;
});

export const authInstance = axios.create({
  baseURL: window.conf.restApiBaseUrl,
  timeout: 10000,
});

authInstance.interceptors.request.use(function(config) {
  config.headers['Content-Type'] = 'application/vnd.api+json';
  config.headers['Accept'] = 'application/vnd.api+json';
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
