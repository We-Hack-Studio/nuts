import {authInstance} from "@/axiosService";

export async function getRobotsIdStrategySpecView(robotId) {
    return authInstance.get(`/robots/${robotId}/strategySpecView/`);
}

export async function patchRobotsIdStrategyParameters(robotId, data) {
    return authInstance.patch(`/robots/${robotId}/strategyParameters/`, data);
}

export async function getRobotDetail(robotId) {
    return authInstance.get(`/robots/${robotId}/`);
}


export async function createRobot(data) {
    return authInstance.post('/robots/', data);
}