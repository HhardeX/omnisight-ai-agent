import apiRequest from "./apiClient";

export async function getBuilds() {
  return apiRequest("/api/v1/builds");
}
