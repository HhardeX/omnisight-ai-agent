import apiRequest from "./apiClient";

export async function getScreenshots() {
  return apiRequest("/api/v1/screenshots");
}
