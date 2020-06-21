import {annonInstance, authInstance} from '../axiosService'

export function login(credentials) {
    return annonInstance.post('/login/', {
        'username': credentials.username,
        'password': credentials.password,
    })
}

export function getExchangeList() {
    return annonInstance.get('/exchanges/')
}

export function getCredentialList() {
    return authInstance.get('/credentials/')
}

export function createCredential(data) {
    return authInstance.post('/credentials/', data)
}

export function deleteCredential(credId) {
    return authInstance.delete('/credentials/' + credId + '/')
}

export function createRobot(data) {
    return authInstance.post('/robots/', data)
}

export function getRobotList() {
    return authInstance.get('/robots/')
}

export function getGridList(robotId) {
    return authInstance.get('/robots/' + robotId + '/grids/')
}

export function createGrids(robotId, data) {
    return authInstance.post('/robots/' + robotId + '/grids/make/', data)
}

export function clearGrids(robotId) {
    return authInstance.delete('/robots/' + robotId + '/grids/clear/')
}