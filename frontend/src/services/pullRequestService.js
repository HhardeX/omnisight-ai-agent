import apiRequest from "./apiClient";

export async function getPullRequests() {
  return apiRequest("/api/v1/pull-requests");
}
