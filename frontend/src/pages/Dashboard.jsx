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

  const build = dashboardData?.latest_build;

  return (
    <>
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

        {isLoading && (
          <p role="status">
            Loading dashboard data...
          </p>
        )}

        {error && (
          <p role="alert">
            Unable to load dashboard data from the backend.
          </p>
        )}

        <div className="stats-grid">
          <article className="stat-card">
            <div className="stat-card-top">
              <div className="stat-icon" aria-hidden="true">
                ▪
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

        <article className="latest-build">
          <div className="latest-build-header">
            <div>
              <span className="latest-build-label">
                Latest Build
              </span>

              <h3>
                {build?.job_id
                  ? `Build ${build.job_id}`
                  : "No builds yet"}
              </h3>

              <p>
                {build?.target_url || "No target URL available"}{" "}
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
                {build ? "Completed" : "No data"}
              </span>
            </div>
          </div>

          <div className="build-divider" />

          <div className="build-metrics">
            <div className="build-metric">
              <span>DOM Size</span>

              <strong>
                {build?.dom_size ?? "-"}
              </strong>
            </div>

            <div className="build-metric success">
              <span>Passed</span>

              <strong>
                {build ? "Yes" : "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>Failed</span>

              <strong>
                {build ? "0" : "-"}
              </strong>
            </div>

            <div className="build-metric">
              <span>UI Issues</span>

              <strong>
                {stats.uiIssues}
              </strong>
            </div>
          </div>
        </article>
      </section>
    </>
  );
}

export default Dashboard;