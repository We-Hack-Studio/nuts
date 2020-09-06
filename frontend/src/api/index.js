import { annonInstance, authInstance } from '@/axiosService';

export async function postAuthLogin(data) {
  return annonInstance.post('/auth/login/?include=user', data);
}

export async function getUsersMe() {
  return authInstance.get('/users/me/');
}

export async function getExchanges() {
  return annonInstance.get('/exchanges/');
}

export async function getCredentials() {
  return await authInstance.get('/credentials/?include=exchange');
}

export async function postCredentials(data) {
  return authInstance.post('/credentials/', data);
}

export async function deleteCredentialsId(credId) {
  return authInstance.delete('/credentials/' + credId + '/');
}

export async function postRobots(data) {
  return authInstance.post('/robots/', data);
}

export async function patchRobotsId(robotId, data) {
  return authInstance.patch('/robots/' + robotId + '/', data);
}

export async function deleteRobotsId(robotId) {
  return authInstance.delete('/robots/' + robotId + '/');
}

export async function getRobotsId(robotId) {
  return authInstance.get('/robots/' + robotId + '/');
}

export async function getRobots() {
  return authInstance.get('/robots/');
}

export async function getStrategies() {
  return authInstance.get('/strategies/');
}

export async function postStrategies(data) {
  return authInstance.post('/strategies/', data);
}

export async function postRobotsIdStrategyParameters(robotId, data) {
  return authInstance.post(`/robots/${robotId}/strategyParameters/`, data);
}
