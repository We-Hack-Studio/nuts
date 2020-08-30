import axios from 'axios'
import store from "./store";

export const annonInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});

export const authInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});
authInstance.interceptors.request.use(function (config) {
    if (store.state.authToken) {
        config.headers = {"Authorization": "Token " + store.state.authToken}
    }
    return config;
});