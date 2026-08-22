const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

async function request(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();

    throw new Error(
      message || `Request failed with status ${response.status}`
    );
  }

  return response.json();
}

export const api = {
  getDashboard: () => request("/dashboard"),

  getBuilds: () => request("/builds"),

  getIssues: () => request("/issues"),

  getScreenshots: () => request("/screenshots"),

  createBuildEvent: (payload) =>
    request("/build-event", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};