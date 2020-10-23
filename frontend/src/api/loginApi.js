import { annonInstance } from '@/axiosService';

export async function postAuthLogin(data) {
    return annonInstance.post('/auth/login/', data);
}
