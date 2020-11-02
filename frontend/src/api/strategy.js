import {authInstance} from "@/axiosService";

export async function getStrategies() {
    return authInstance.get('/strategies/');
}

export async function createStrategy(data) {
    return authInstance.post('/strategies/', data);
}