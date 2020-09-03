import Kitsu from 'kitsu'
import store from "./store";


export const annonInstance = new Kitsu({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 5000,
    resourceCase: 'snake',
});

export const authInstance = new Kitsu({
    baseURL: window.conf.restApiBaseUrl,
    timeout: 5000,
});

authInstance.interceptors.request.use(function (config) {
    if (store.state.authToken) {
        config.headers["Authorization"] = store.state.authToken
    }
    return config;
});