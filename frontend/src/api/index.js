import { annonInstance, authInstance } from "../axiosService";

export function login(credentials) {
  return annonInstance.post("/login/", {
    username: credentials.username,
    password: credentials.password,
  });
}

export function getExchangeList() {
  return annonInstance.get("/exchanges/");
}

export function getCredentialList() {
  return authInstance.get("/credentials/");
}

export function createCredential(data) {
  return authInstance.post("/credentials/", data);
}

export function deleteCredential(credId) {
  return authInstance.delete("/credentials/" + credId + "/");
}

export function createRobot(data) {
  return authInstance.post("/robots/", data);
}

export function updateRobot(robotId, data) {
  return authInstance.patch("/robots/" + robotId + "/", data);
}

export function getRobot(robotId) {
  return authInstance.get("/robots/" + robotId + "/");
}

export function getRobotList() {
  return authInstance.get("/robots/");
}

export function getGridList(robotId) {
  return authInstance.get("/robots/" + robotId + "/grids/");
}

export function createGrids(robotId, data) {
  return authInstance.post("/robots/" + robotId + "/grids/make/", data);
}

export function clearGrids(robotId) {
  return authInstance.delete("/robots/" + robotId + "/grids/clear/");
}

export function getStrategyTemplateList() {
  return authInstance.get("/strategy-templates/");
}

export function createStrategyTemplate(data) {
  return authInstance.post("/strategy-templates/", data);
}

export function updateRobotStrategyParams(robotId, data) {
  return authInstance.post(`/robots/${robotId}/strategy_parameters/`, {
    strategy_parameters_fields: JSON.stringify(data),
  });
}
