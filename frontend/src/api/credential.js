import {authInstance} from "@/axiosService";

export async function getCredentials() {
    return await authInstance.get('/credentials/');
}

export async function createCredential(data) {
    return authInstance.post('/credentials/', data);
}

export async function deleteCredential(credId) {
    return authInstance.delete('/credentials/' + credId + '/');
}

export async function updateCredential(credId, data) {
    return authInstance.patch('/credentials/' + credId + '/', data);
}