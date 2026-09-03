
import { useCallback, useEffect, useState } from "react";
import { getDashboardData } from "../services/dashboardService";

function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const loadDashboard = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setIsRefreshing(true);
      } else {
        setIsLoading(true);
      }

      setError(null);

      const data = await getDashboardData();

      setDashboardData(data);
    } catch (err) {
      setError(err.message || "Unable to load dashboard data.");
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const stats = {
    totalBuilds: dashboardData?.total_builds ?? 0,
    uiIssues: dashboardData?.total_issues ?? 0,
    totalScreenshots: dashboardData?.total_screenshots ?? 0,
  };

  const backendBuild = dashboardData?.latest_build;

  const build = backendBuild
    ? {
        id: backendBuild.job_id,
        deployment: backendBuild.target_url,
        viewport: backendBuild.viewport,
        domSize: backendBuild.dom_size,
        status: "Completed",
        issues: stats.uiIssues,
      }
    : null;

  return (
    <>
      {/* Dashboard Header */}
      <header className="dashboard-header">
        <div>
          <h1>Dashboard</h1>
          <p>OmniSight QA overview</p>
        </div>

        <div
          className="environment"
          aria-label="Current environment: Staging"
        >
          <span className="status-dot" aria-hidden="true" />
          <span>Staging</span>
        </div>
      </header>

      {/* Dashboard Content */}
      <section className="dashboard-content">
        <div className="section-heading">
          <div>
            <h2>Overview</h2>
            <p>Monitor your automated UI testing activity.</p>
          </div>

          <button
            type="button"
            onClick={() => loadDashboard(true)}
            disabled={isRefreshing}
          >
            {isRefreshing ? "Refreshing..." : "Refresh"}
          </button>
        </div>

        {/* Loading State */}
        {isLoading && (
          <p role="status">
            Loading dashboard data...
          </p>
        )}

        {/* Error State */}
        {error && (
          <p role="alert">
            Unable to load dashboard data from the backend.
          </p>
        )}

        {/* Statistics */}
        <div className="stats-grid">
          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                ▦
              </div>

              <span className="stat-label">
                Total Builds
              </span>
            </div>

            <strong className="stat-value">
              {stats.totalBuilds}
            </strong>

            <span className="stat-meta">
              Automated UI audits
            </span>
          </article>

          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                !
              </div>

              <span className="stat-label">
                UI Issues
              </span>
            </div>

            <strong className="stat-value">
              {stats.uiIssues}
            </strong>

            <span className="stat-meta">
              Issues detected
            </span>
          </article>

          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                ▣
              </div>

              <span className="stat-label">
                Screenshots
              </span>
            </div>

            <strong className="stat-value">
              {stats.totalScreenshots}
            </strong>

            <span className="stat-meta">
              Captured during audits
            </span>
          </article>
        </div>

        {/* Latest Build */}
        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              <h3>
                {build?.id
                  ? `Build ${build.id}`
                  : "No builds yet"}
              </h3>

              <p>
                {build?.deployment || "No target URL available"}{" "}
                •{" "}
                {build?.viewport || "No viewport available"}
              </p>
            </div>

            <div className="build-status">
              <span
                className="build-status-dot"
                aria-hidden="true"
              />

              <span>
                {build?.status || "No build"}
              </span>
            </div>
          </div>

          <div className="build-divider" />

          {/* Latest Build Metrics */}
          <div className="build-metrics">
            <div className="build-metric">
              <span>DOM Size</span>

              <strong>
                {build?.domSize ?? "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>Viewport</span>

              <strong>
                {build?.viewport || "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>

              <strong>
                {build?.issues ?? 0}
              </strong>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}

export default Dashboard;

