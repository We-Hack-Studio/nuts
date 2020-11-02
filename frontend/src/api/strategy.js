import {authInstance} from "@/axiosService";

export async function getStrategies() {
    return authInstance.get('/strategies/');
}