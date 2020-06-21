import axios from 'axios'
import store from "./store";

export const annonInstance = axios.create({
    baseURL: window.conf.apiBaseUrl,
    timeout: 10000,
});

export const authInstance = axios.create({
    baseURL: window.conf.apiBaseUrl,
    timeout: 10000,
});
authInstance.interceptors.request.use(function (config) {
    if (store.state.user.token) {
        config.headers = {"Authorization": "Token " + store.state.user.token}
    }
    return config;
});