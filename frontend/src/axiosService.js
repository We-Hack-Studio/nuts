import axios from 'axios'
import store from "./store";

export const annonInstance = axios.create({
    baseURL: "http://127.0.0.1:7000/api",
    timeout: 10000,
});

export const authInstance = axios.create({
    baseURL: "http://127.0.0.1:7000/api",
    timeout: 10000,
});
authInstance.interceptors.request.use(function (config) {
    if (store.state.user.token) {
        config.headers = {"Authorization": "Token " + store.state.user.token}
    }
    return config;
});