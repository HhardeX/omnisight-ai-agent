import apiRequest from "./apiClient";

export async function getIssues() {
  return apiRequest("/api/v1/issues");
}
