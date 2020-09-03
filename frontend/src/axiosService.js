import axios from 'axios'
import store from "./store";

export const annonInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});
annonInstance.interceptors.request.use(function (config) {
    config.headers["Content-Type"] = "application/vnd.api+json"
    config.headers["Accept"] = "application/vnd.api+json"
    return config;
});

export const authInstance = axios.create({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 10000,
});
authInstance.defaults.headers.common['Content-Type'] = "application/vnd.api+json"
authInstance.defaults.headers.common['Accept'] = "application/vnd.api+json"
authInstance.interceptors.request.use(function (config) {
    if (store.state.authToken) {
        config.headers["Authorization"] = store.state.authToken
    }
    return config;
});