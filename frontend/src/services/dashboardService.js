import apiRequest from "./apiClient";

export async function getDashboardData() {
  return apiRequest("/api/dashboard");
}
