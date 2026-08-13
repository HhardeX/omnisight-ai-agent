// =========================================================
// OmniSight - Centralized Mock Data
// =========================================================

// =========================================================
// Builds
// =========================================================

export const builds = [
  {
    id: "#124",
    deployment: "Staging deployment",
    time: "2 minutes ago",
    tests: 18,
    passed: 18,
    failed: 0,
    issues: 0,
    status: "Passed",
  },
  {
    id: "#123",
    deployment: "Staging deployment",
    time: "28 minutes ago",
    tests: 16,
    passed: 16,
    failed: 0,
    issues: 0,
    status: "Passed",
  },
  {
    id: "#122",
    deployment: "Staging deployment",
    time: "1 hour ago",
    tests: 20,
    passed: 19,
    failed: 1,
    issues: 1,
    status: "Failed",
  },
];

// =========================================================
// Dashboard Statistics
// =========================================================

export const dashboardStats = {
  totalBuilds: 12,
  passedBuilds: 10,
  uiIssues: 2,
  buildsThisWeek: 3,
  successRate: 83,
};

// =========================================================
// Latest Build
// =========================================================

export const latestBuild = {
  id: "#124",
  deployment: "Staging deployment",
  time: "2 minutes ago",
  status: "Passed",
  tests: 18,
  passed: 18,
  failed: 0,
  issues: 0,
};

// =========================================================
// Issues
// =========================================================

export const issues = [
  {
    id: "ISSUE-001",
    title: "Login button alignment issue",
    description:
      "The login button is slightly misaligned on the authentication page.",
    page: "Login page",
    build: "#122",
    severity: "High",
    status: "Open",
    detected: "1 hour ago",
  },
  {
    id: "ISSUE-002",
    title: "Mobile navigation overflow",
    description:
      "Navigation items extend beyond the viewport on smaller screen sizes.",
    page: "Dashboard",
    build: "#121",
    severity: "Medium",
    status: "Open",
    detected: "3 hours ago",
  },
  {
    id: "ISSUE-003",
    title: "Incorrect button spacing",
    description:
      "The spacing between secondary action buttons does not match the expected layout.",
    page: "Settings",
    build: "#120",
    severity: "Low",
    status: "Resolved",
    detected: "Yesterday",
  },
];

export const issueStats = {
  total: 3,
  open: 2,
  resolved: 1,
};

// =========================================================
// Screenshots
// =========================================================

export const screenshots = [
  {
    id: "SHOT-001",
    title: "Login page",
    page: "Login",
    build: "#124",
    status: "Passed",
    time: "2 minutes ago",
    description: "Latest staging screenshot captured during automated testing.",
  },
  {
    id: "SHOT-002",
    title: "Dashboard overview",
    page: "Dashboard",
    build: "#123",
    status: "Passed",
    time: "28 minutes ago",
    description: "Dashboard layout verified successfully.",
  },
  {
    id: "SHOT-003",
    title: "Settings page",
    page: "Settings",
    build: "#122",
    status: "Issue detected",
    time: "1 hour ago",
    description: "Visual difference detected in the settings layout.",
  },
  {
    id: "SHOT-004",
    title: "Mobile navigation",
    page: "Dashboard",
    build: "#121",
    status: "Issue detected",
    time: "3 hours ago",
    description: "Navigation overflow detected at mobile viewport size.",
  },
];

export const screenshotStats = {
  total: 24,
  verified: 22,
  visualIssues: 2,
};

// =========================================================
// Pull Requests
// =========================================================

export const pullRequests = [
  {
    id: "#142",
    title: "Improve checkout flow UI",
    branch: "feature/checkout-ui",
    author: "Abhijeet",
    time: "12 minutes ago",
    status: "Passed",
    checks: 18,
    issues: 0,
  },
  {
    id: "#141",
    title: "Update authentication screens",
    branch: "feature/auth-ui",
    author: "Hardev",
    time: "1 hour ago",
    status: "Passed",
    checks: 16,
    issues: 0,
  },
  {
    id: "#140",
    title: "Fix responsive dashboard layout",
    branch: "fix/dashboard-responsive",
    author: "Developer",
    time: "3 hours ago",
    status: "Review",
    checks: 20,
    issues: 1,
  },
];
